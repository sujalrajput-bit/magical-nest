"""Deterministic conversation state machine.

Defines the allowed transitions between call states.
"""

from mn_ai_voice.app.core.constants import CallState

class StateMachine:
    """
    Pure deterministic conversation flow.
    No DB. No text parsing.
    """

    _flow = [
        CallState.ASK_LANGUAGE,
        CallState.ASK_CITY_OR_REGION,
        CallState.ASK_REGION_CONFIRM,
        CallState.ASK_TIMELINE,
        CallState.ASK_BUDGET,
        CallState.ASK_ROOM_SIZE,
        CallState.QUALIFY,
        CallState.ASK_EMAIL,
        CallState.CLOSE,
    ]

    def next_state(self, current: CallState) -> CallState:
        """Return the next conversation state given the current state."""

        index = self._flow.index(current)
        return self._flow[min(index + 1, len(self._flow) - 1)]
