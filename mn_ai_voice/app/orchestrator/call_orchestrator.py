"""
Call orchestration logic.

Coordinates a single user turn by routing input, updating state,
applying skills, and emitting events.
"""

from sqlalchemy.orm import Session

from mn_ai_voice.app.engine.state_machine import StateMachine
from mn_ai_voice.app.engine.prompt_templates import PromptRenderer
from mn_ai_voice.app.skills.faq_skill import FAQSkill
from mn_ai_voice.app.skills.qualification_skill import QualificationSkill
from mn_ai_voice.app.core.constants import EventType, CallState, QualificationStatus
from mn_ai_voice.app.db.models import Event, Call, LeadSnapshot


class CallOrchestrator:
    """Coordinates a single conversational turn for a call."""

    def __init__(self) -> None:
        self.state_machine = StateMachine()
        self.prompts = PromptRenderer()
        self.faq = FAQSkill()
        self.qualification = QualificationSkill()

    def handle_turn(
        self,
        db: Session,
        call: Call,
        snapshot: LeadSnapshot,
        text: str,
    ) -> str:
        """Handle one user turn and return the assistant reply."""

        # --- Log user input ---
        db.add(
            Event(
                call_id=call.call_id,
                type=EventType.USER_TURN,
                payload={"text": text},
            )
        )

        # --- FAQ interrupt (no state mutation) ---
        if self.faq.can_handle(text):
            answer = self.faq.handle(type("Ctx", (), {"text": text}))
            if answer:
                db.add(
                    Event(
                        call_id=call.call_id,
                        type=EventType.ASSISTANT_TURN,
                        payload={"text": answer},
                    )
                )
                return answer

        # --- Apply qualification skill ---
        current_state = CallState(call.current_state)
        snapshot = self.qualification.apply(current_state, text, snapshot)

        # --- Derive snapshot signals ---
        has_timeline = snapshot.timeline_bucket not in {None, "unknown"}
        has_room_size = bool(snapshot.room_size_text)

        qualification_status = None
        if snapshot.qualification_status:
            try:
                qualification_status = QualificationStatus(snapshot.qualification_status)
            except ValueError:
                qualification_status = None

        # --- Determine next state ---
        next_state = self.state_machine.next_state(
            current_state,
            has_timeline=has_timeline,
            has_room_size=has_room_size,
            qualification_status=qualification_status,
        )

        call.current_state = next_state.value

        # --- Render assistant reply ---
        reply = self.prompts.render(next_state)

        db.add(
            Event(
                call_id=call.call_id,
                type=EventType.ASSISTANT_TURN,
                payload={"text": reply},
            )
        )

        return reply
