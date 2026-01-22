"""Call lifecycle API routes."""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mn_ai_voice.app.db.models import Call, Lead, LeadSnapshot, Event
from mn_ai_voice.app.orchestrator.call_orchestrator import CallOrchestrator
from mn_ai_voice.app.core.constants import CallState, CallStatus, EventType
from mn_ai_voice.app.api.dependencies import get_db
from mn_ai_voice.app.api.schemas import UserTurnRequest

router = APIRouter()
orchestrator = CallOrchestrator()


@router.post("/start")
def start_call(
    from_phone: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Start a new call session.

    - Reuses Lead identity by phone
    - Reuses LeadSnapshot per lead
    - Creates a new Call per session
    - Emits CALL_STARTED event
    """

    # --- Find or create Lead ---
    lead = (
        db.query(Lead)
        .filter(Lead.primary_phone == from_phone)
        .one_or_none()
    )

    if lead is None:
        lead = Lead(
            lead_id=f"l_{uuid.uuid4().hex[:8]}",
            primary_phone=from_phone,
        )
        db.add(lead)
        db.flush()

        # Create snapshot ONCE per lead
        snapshot = LeadSnapshot(lead_id=lead.lead_id)
        db.add(snapshot)

    # --- Create Call ---
    call = Call(
        call_id=f"c_{uuid.uuid4().hex[:8]}",
        lead_id=lead.lead_id,
        from_phone=from_phone,
        direction="inbound",
        status=CallStatus.IN_PROGRESS.value,
        current_state=CallState.ASK_LANGUAGE.value,
    )
    db.add(call)
    db.flush()

    # --- Emit CALL_STARTED event ---
    db.add(
        Event(
            call_id=call.call_id,
            type=EventType.CALL_STARTED.value,
            payload_json={"from_phone": from_phone},
        )
    )

    db.commit()

    return {
        "call_id": call.call_id,
        "next_prompt": {
            "text": "Would you like to speak in English, Hindi, or Hinglish?"
        },
    }


@router.post("/{call_id}/user_turn")
def user_turn(
    call_id: str,
    payload: UserTurnRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Handle a single user turn.

    Idempotent via turn_id.
    """

    call = db.get(Call, call_id)
    if call is None:
        raise HTTPException(status_code=404, detail="Call not found")

    snapshot = (
        db.query(LeadSnapshot)
        .filter(LeadSnapshot.lead_id == call.lead_id)
        .one_or_none()
    )
    if snapshot is None:
        raise HTTPException(status_code=500, detail="Lead snapshot missing")

    # --- Idempotency check ---
    existing = (
        db.query(Event)
        .filter(
            Event.call_id == call_id,
            Event.type == EventType.USER_TURN.value,
            Event.payload_json["turn_id"].as_string() == payload.turn_id,
        )
        .one_or_none()
    )

    if existing:
        return {
            "assistant": {"text": "Already processed"},
            "state": call.current_state,
        }

    reply = orchestrator.handle_turn(db, call, snapshot, payload.text)
    db.commit()

    return {
        "assistant": {"text": reply},
        "state": call.current_state,
    }
