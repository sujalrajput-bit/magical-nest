"""Call lifecycle API routes."""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mn_ai_voice.app.db.models import Call, Lead, LeadSnapshot
from mn_ai_voice.app.orchestrator.call_orchestrator import CallOrchestrator
from mn_ai_voice.app.core.constants import CallState, CallStatus
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

    Reuses lead identity if phone already exists.
    """
    # --- Find or create lead ---
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
        db.flush()  # ensure lead_id available

        snapshot = LeadSnapshot(lead_id=lead.lead_id)
        db.add(snapshot)
    else:
        snapshot = db.get(LeadSnapshot, lead.lead_id)
        if snapshot is None:
            snapshot = LeadSnapshot(lead_id=lead.lead_id)
            db.add(snapshot)

    # --- Create call ---
    call_id = f"c_{uuid.uuid4().hex[:8]}"
    call = Call(
        call_id=call_id,
        lead_id=lead.lead_id,
        from_phone=from_phone,
        status=CallStatus.IN_PROGRESS.value,
        current_state=CallState.ASK_LANGUAGE.value,
    )

    db.add(call)
    db.commit()

    return {
        "call_id": call_id,
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
    """Handle a single user turn for an active call."""

    call = db.get(Call, call_id)
    if call is None:
        raise HTTPException(status_code=404, detail="Call not found")

    snapshot = db.get(LeadSnapshot, call.lead_id)
    if snapshot is None:
        raise HTTPException(status_code=500, detail="Lead snapshot missing")

    reply = orchestrator.handle_turn(db, call, snapshot, payload.text)
    db.commit()

    return {
        "assistant": {"text": reply},
        "state": call.current_state,
    }
