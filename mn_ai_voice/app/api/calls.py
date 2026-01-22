"""Call lifecycle API routes."""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mn_ai_voice.app.db.models import Call, LeadSnapshot
from mn_ai_voice.app.orchestrator.call_orchestrator import CallOrchestrator
from mn_ai_voice.app.core.constants import CallState, CallStatus
from mn_ai_voice.app.api.dependencies import get_db
from mn_ai_voice.app.api.schemas import UserTurnRequest

router = APIRouter()
orchestrator = CallOrchestrator()


@router.post("/start")
def start_call(db: Session = Depends(get_db)) -> dict:
    """Start a new call session and return the first prompt."""
    call_id = f"c_{uuid.uuid4().hex[:8]}"

    call = Call(
        call_id=call_id,
        status=CallStatus.IN_PROGRESS.value,
        current_state=CallState.ASK_LANGUAGE.value,
    )
    snapshot = LeadSnapshot(call_id=call_id)

    db.add_all([call, snapshot])
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
    snapshot = db.get(LeadSnapshot, call_id)

    if call is None or snapshot is None:
        raise HTTPException(status_code=404, detail="Call not found")

    reply = orchestrator.handle_turn(db, call, snapshot, payload.text)
    db.commit()

    return {
        "assistant": {"text": reply},
        "state": call.current_state,
    }
