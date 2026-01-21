"""Application-wide enumerations and constants.

Defines enums used for call lifecycle, conversation flow,
event tracking, and lead qualification.
"""

from enum import Enum

class CallStatus(str, Enum):
    """Represents the lifecycle status of a phone call."""

    IN_PROGRESS = "in_progress"
    ENDED = "ended"
    FAILED = "failed"

class CallState(str, Enum):
    """Represents the conversational state within a call flow."""

    ASK_LANGUAGE = "ASK_LANGUAGE"
    ASK_CITY_OR_REGION = "ASK_CITY_OR_REGION"
    ASK_REGION_CONFIRM = "ASK_REGION_CONFIRM"
    ASK_TIMELINE = "ASK_TIMELINE"
    ASK_BUDGET = "ASK_BUDGET"
    ASK_ROOM_SIZE = "ASK_ROOM_SIZE"
    QUALIFY = "QUALIFY"
    ASK_EMAIL = "ASK_EMAIL"
    CLOSE = "CLOSE"

class EventType(str, Enum):
    """Represents discrete events emitted during a call."""

    CALL_STARTED = "call_started"
    USER_TURN = "user_turn"
    ASSISTANT_TURN = "assistant_turn"
    CALL_ENDED = "call_ended"

class QualificationStatus(str, Enum):
    """Represents the final qualification outcome for a lead."""

    UNKNOWN = "unknown"
    QUALIFIED = "qualified"
    NURTURE = "nurture"
    UNQUALIFIED = "unqualified"

class QualificationReason(str, Enum):
    """Represents reasons a lead may not qualify."""

    REGION_NOT_SERVED = "REGION_NOT_SERVED"
    BUDGET_BELOW_MIN = "BUDGET_BELOW_MIN"
    BUDGET_ABOVE_BAND = "BUDGET_ABOVE_BAND"
