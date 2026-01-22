"""
Deterministic conversation state machine.

Defines allowed transitions between call states.
Supports conditional and non-linear progression.
"""

from typing import Optional

from mn_ai_voice.app.core.constants import CallState, QualificationStatus


class StateMachine:
    """
    Deterministic conversation flow controller.

    - First three states are strictly linear
    - Timeline and room size are optional
    - Qualification result determines whether email is asked
    """

    def next_state(
        self,
        current: CallState,
        has_timeline: bool = False,
        has_room_size: bool = False,
        qualification_status: Optional[QualificationStatus] = None,
    ) -> CallState:
        """
        Return the next conversation state based on current state
        and known snapshot information.

        Args:
            current: Current conversation state
            has_timeline: Whether timeline is already known
            has_room_size: Whether room size is already known
            qualification_status: Result after QUALIFY (if available)

        Returns:
            Next CallState
        """

        # --- Mandatory linear flow ---
        if current == CallState.ASK_LANGUAGE:
            return CallState.ASK_CITY_OR_REGION

        if current == CallState.ASK_CITY_OR_REGION:
            return CallState.ASK_REGION_CONFIRM

        if current == CallState.ASK_REGION_CONFIRM:
            return CallState.ASK_BUDGET

        # --- Optional steps ---
        if current == CallState.ASK_BUDGET:
            if not has_timeline:
                return CallState.ASK_TIMELINE
            if not has_room_size:
                return CallState.ASK_ROOM_SIZE
            return CallState.QUALIFY

        if current == CallState.ASK_TIMELINE:
            if not has_room_size:
                return CallState.ASK_ROOM_SIZE
            return CallState.QUALIFY

        if current == CallState.ASK_ROOM_SIZE:
            return CallState.QUALIFY

        # --- Qualification decision ---
        if current == CallState.QUALIFY:
            if qualification_status in {
                QualificationStatus.QUALIFIED,
                QualificationStatus.NURTURE,
            }:
                return CallState.ASK_EMAIL
            return CallState.CLOSE

        # --- Terminal states ---
        if current in {CallState.ASK_EMAIL, CallState.CLOSE}:
            return CallState.CLOSE

        # Fallback safety
        return CallState.CLOSE
