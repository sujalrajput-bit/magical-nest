"""
Unit tests for the conversation state machine.

These tests ensure deterministic and correct
state transitions for the call flow.
"""

from mn_ai_voice.app.engine.state_machine import StateMachine
from mn_ai_voice.app.core.constants import CallState


def test_initial_state_progression():
    """
    ASK_LANGUAGE → ASK_CITY_OR_REGION
    """
    sm = StateMachine()

    next_state = sm.next_state(CallState.ASK_LANGUAGE)

    assert next_state == CallState.ASK_CITY_OR_REGION


def test_middle_state_progression():
    """
    ASK_BUDGET → ASK_ROOM_SIZE
    """
    sm = StateMachine()

    next_state = sm.next_state(CallState.ASK_BUDGET)

    assert next_state == CallState.ASK_ROOM_SIZE


def test_final_state_is_terminal():
    """
    CLOSE should remain CLOSE (terminal state)
    """
    sm = StateMachine()

    next_state = sm.next_state(CallState.CLOSE)

    assert next_state == CallState.CLOSE
