"""Tests for application-wide enum definitions."""

import pytest

from mn_ai_voice.app.core.constants import (
    CallStatus,
    CallState,
    EventType,
    QualificationStatus,
    QualificationReason,
)


def test_call_status_values():
    """Verify CallStatus enum values."""

    assert CallStatus.IN_PROGRESS.value == "in_progress"
    assert CallStatus.ENDED.value == "ended"
    assert CallStatus.FAILED.value == "failed"


def test_call_state_values():
    """Verify CallState enum values."""

    assert CallState.ASK_LANGUAGE.value == "ASK_LANGUAGE"
    assert CallState.ASK_CITY_OR_REGION.value == "ASK_CITY_OR_REGION"
    assert CallState.ASK_REGION_CONFIRM.value == "ASK_REGION_CONFIRM"
    assert CallState.ASK_TIMELINE.value == "ASK_TIMELINE"
    assert CallState.ASK_BUDGET.value == "ASK_BUDGET"
    assert CallState.ASK_ROOM_SIZE.value == "ASK_ROOM_SIZE"
    assert CallState.QUALIFY.value == "QUALIFY"
    assert CallState.ASK_EMAIL.value == "ASK_EMAIL"
    assert CallState.CLOSE.value == "CLOSE"


def test_event_type_values():
    """Verify EventType enum values."""

    assert EventType.CALL_STARTED.value == "call_started"
    assert EventType.USER_TURN.value == "user_turn"
    assert EventType.ASSISTANT_TURN.value == "assistant_turn"
    assert EventType.CALL_ENDED.value == "call_ended"


def test_qualification_status_values():
    """Verify QualificationStatus enum values."""

    assert QualificationStatus.UNKNOWN.value == "unknown"
    assert QualificationStatus.QUALIFIED.value == "qualified"
    assert QualificationStatus.NURTURE.value == "nurture"
    assert QualificationStatus.UNQUALIFIED.value == "unqualified"


def test_qualification_reason_values():
    """
    Verify QualificationReason enum values.

    Stored as lowercase strings for DB compatibility.
    """

    assert QualificationReason.REGION_NOT_SERVED.value == "region_not_served"
    assert QualificationReason.BUDGET_BELOW_MIN.value == "budget_below_min"
    assert QualificationReason.BUDGET_ABOVE_BAND.value == "budget_above_band"


def test_enum_string_comparison():
    """Ensure enums behave like strings."""

    assert CallStatus.IN_PROGRESS == "in_progress"
    assert EventType.CALL_STARTED == "call_started"
    assert QualificationReason.REGION_NOT_SERVED == "region_not_served"


def test_invalid_enum_value_raises_error():
    """Invalid enum values should raise ValueError."""

    with pytest.raises(ValueError):
        CallStatus("invalid")

    with pytest.raises(ValueError):
        CallState("INVALID_STATE")

    with pytest.raises(ValueError):
        QualificationReason("INVALID_REASON")
