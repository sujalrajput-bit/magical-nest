from mn_ai_voice.app.engine.state_machine import StateMachine
from mn_ai_voice.app.engine.prompt_templates import PromptRenderer
from mn_ai_voice.app.skills.faq_skill import FAQSkill
from mn_ai_voice.app.skills.qualification_skill import QualificationSkill
from mn_ai_voice.app.core.constants import EventType, CallState
from mn_ai_voice.app.db.models import Event


class CallOrchestrator:
    """
    Coordinates ONE user turn.
    No HTTP. No DB queries outside repositories.
    """

    def __init__(self):
        self.state_machine = StateMachine()
        self.prompts = PromptRenderer()
        self.faq = FAQSkill()
        self.qualification = QualificationSkill()

    def handle_turn(self, db, call, snapshot, text: str) -> str:
        db.add(Event(call_id=call.call_id, type=EventType.USER_TURN, payload={"text": text}))

        if self.faq.can_handle(text):
            answer = self.faq.handle(type("Ctx", (), {"text": text}))
            db.add(Event(call_id=call.call_id, type=EventType.ASSISTANT_TURN, payload={"text": answer}))
            return answer

        current_state = CallState(call.current_state)
        snapshot = self.qualification.apply(current_state, text, snapshot)

        next_state = self.state_machine.next_state(current_state)
        call.current_state = next_state.value

        reply = self.prompts.render(next_state)
        db.add(Event(call_id=call.call_id, type=EventType.ASSISTANT_TURN, payload={"text": reply}))

        return reply
