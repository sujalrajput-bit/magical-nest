"""
Database ORM models for MN-AI-Voice.

Defines SQLAlchemy models used for lead identity,
call tracking, event logging, artifacts, and CRM outbox.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    JSON,
    Integer,
    ForeignKey,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


# =========================
# Lead Identity
# =========================

class Lead(Base):
    """
    Represents a persistent lead identity.

    A lead may have multiple calls over time.
    """

    __tablename__ = "leads"

    lead_id = Column(String, primary_key=True)
    primary_phone = Column(String, unique=True, nullable=False)
    primary_email = Column(String, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


# =========================
# Call Session
# =========================

class Call(Base):
    """Represents a phone call session."""

    __tablename__ = "calls"

    call_id = Column(String, primary_key=True)
    lead_id = Column(String, ForeignKey("leads.lead_id"), nullable=True)

    from_phone = Column(String)
    direction = Column(String, nullable=False, default="inbound")
    language_pref = Column(String, nullable=True)

    status = Column(String)        # CallStatus enum value
    current_state = Column(String) # CallState enum value

    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime, nullable=True)

    source = Column(String)


# =========================
# Event Ledger (Immutable)
# =========================

class Event(Base):
    """
    Immutable event log for a call.

    No idempotency — every event is recorded.
    """

    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True)
    call_id = Column(String, ForeignKey("calls.call_id"), nullable=False)

    type = Column(String)  # EventType enum value
    payload_json = Column(JSON)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# =========================
# Lead Snapshot (Identity-level memory)
# =========================

class LeadSnapshot(Base):
    """
    Mutable snapshot of extracted information
    for a single lead identity.
    """

    __tablename__ = "lead_snapshot"

    lead_id = Column(
        String,
        ForeignKey("leads.lead_id"),
        primary_key=True,
    )

    language = Column(String, default="unknown")
    city_text = Column(String, nullable=True)

    region_value = Column(String, default="unknown")
    region_confirmed = Column(Boolean, nullable=True)

    budget_band = Column(String, default="unknown")
    timeline_bucket = Column(String, default="unknown")
    room_size_text = Column(String, nullable=True)

    email = Column(String, nullable=True)

    qualification_status = Column(String, default="unknown")
    qualification_reasons = Column(JSON, default=list, nullable=False)

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


# =========================
# Artifacts
# =========================

class Artifact(Base):
    """
    Generated artifacts such as call summaries.
    """

    __tablename__ = "artifacts"

    artifact_id = Column(Integer, primary_key=True)
    call_id = Column(String, ForeignKey("calls.call_id"), nullable=False)

    type = Column(String)  # summary / extracted_fields
    content_text = Column(String, nullable=True)
    content_json = Column(JSON, nullable=True)

    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# =========================
# CRM Outbox (Idempotent)
# =========================

class CRMOutbox(Base):
    """
    Outbox table for CRM actions.

    Uses idempotency_key to guarantee exactly-once semantics.
    """

    __tablename__ = "crm_outbox"

    outbox_id = Column(Integer, primary_key=True)
    call_id = Column(String, ForeignKey("calls.call_id"), nullable=False)

    action = Column(String)  # upsert_lead / set_stage / append_note
    payload_json = Column(JSON)

    idempotency_key = Column(String, unique=True, nullable=False)

    status = Column(String, default="pending")  # pending / success / failed
    attempts = Column(Integer, default=0)
    last_error = Column(String, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
