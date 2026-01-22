"""
Unit tests for the conversation state machine.

These tests validate mandatory linear progression,
optional steps, and conditional branching.
"""

from mn_ai_voice.app.engine.state_machine import StateMachine
from mn_ai_voice.app.core.constants import CallState, QualificationStatus


def test_mandatory_linear_start():
    """
    ASK_LANGUAGE → ASK_CITY_OR_REGION → ASK_REGION_CONFIRM
    """
    sm = StateMachine()

    state = sm.next_state(CallState.ASK_LANGUAGE)
    assert state == CallState.ASK_CITY_OR_REGION

    state = sm.next_state(CallState.ASK_CITY_OR_REGION)
    assert state == CallState.ASK_REGION_CONFIRM


def test_budget_skips_timeline_when_already_known():
    """
    If timeline is already known, ASK_BUDGET should
    move directly to ASK_ROOM_SIZE or QUALIFY.
    """
    sm = StateMachine()

    next_state = sm.next_state(
        CallState.ASK_BUDGET,
        has_timeline=True,
        has_room_size=False,
    )

    assert next_state == CallState.ASK_ROOM_SIZE


def test_budget_skips_room_size_when_already_known():
    """
    If room size is already known, ASK_BUDGET should
    move directly to ASK_TIMELINE or QUALIFY.
    """
    sm = StateMachine()

    next_state = sm.next_state(
        CallState.ASK_BUDGET,
        has_timeline=False,
        has_room_size=True,
    )

    assert next_state == CallState.ASK_TIMELINE


def test_qualify_routes_to_email_for_qualified():
    """
    QUALIFY → ASK_EMAIL when status is QUALIFIED or NURTURE
    """
    sm = StateMachine()

    next_state = sm.next_state(
        CallState.QUALIFY,
        qualification_status=QualificationStatus.QUALIFIED,
    )

    assert next_state == CallState.ASK_EMAIL


def test_qualify_routes_to_close_for_unqualified():
    """
    QUALIFY → CLOSE when status is UNQUALIFIED
    """
    sm = StateMachine()

    next_state = sm.next_state(
        CallState.QUALIFY,
        qualification_status=QualificationStatus.UNQUALIFIED,
    )

    assert next_state == CallState.CLOSE


def test_close_is_terminal():
    """
    CLOSE should remain CLOSE
    """
    sm = StateMachine()

    next_state = sm.next_state(CallState.CLOSE)

    assert next_state == CallState.CLOSE
