"""
Acceptance tests for FAQ interrupt behavior.

Ensures that FAQ questions do not mutate
the active conversation state.
"""

from mn_ai_voice.app.orchestrator.call_orchestrator import CallOrchestrator
from mn_ai_voice.app.core.constants import CallState
from mn_ai_voice.app.db.models import Call, LeadSnapshot


class DummySession:
    """
    Minimal stub for SQLAlchemy session.
    Collects events but performs no DB operations.
    """

    def __init__(self):
        self.events = []

    def add(self, obj):
        """
        Add an object to the events list for testing purposes.

        Args:
            obj: Object to add to the events collection.
        """
        self.events.append(obj)

    def commit(self):
        """
        No-op commit method for testing purposes.

        This method does nothing since DummySession doesn't perform
        actual database operations.
        """

def test_faq_interrupt_does_not_change_state():
    """
    During ASK_BUDGET, user asks an FAQ.
    → FAQ answer returned
    → Call state remains ASK_BUDGET
    """

    orchestrator = CallOrchestrator()
    db = DummySession()

    call = Call(
        call_id="c_test",
        from_phone="+911234567890",
        status="in_progress",
        current_state=CallState.ASK_BUDGET.value,
    )

    snapshot = LeadSnapshot(call_id="c_test")

    user_text = "What is your process?"

    reply = orchestrator.handle_turn(
        db=db,
        call=call,
        snapshot=snapshot,
        text=user_text,
    )

    # Assert FAQ answer returned
    assert reply is not None
    assert "process" in reply.lower()

    # Assert state unchanged
    assert call.current_state == CallState.ASK_BUDGET.value
