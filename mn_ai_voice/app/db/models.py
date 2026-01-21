"""Database ORM models for MN-AI-Voice.

Defines SQLAlchemy models used for call tracking, event logging,
and lead qualification snapshots.
"""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, DateTime, Boolean, JSON, Integer, ForeignKey, text

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

class Call(Base):
    """Represents a phone call session tracked by the system."""

    __tablename__ = "calls"

    call_id = Column(String, primary_key=True)
    from_phone = Column(String)
    status = Column(String)
    current_state = Column(String)
    started_at = Column(DateTime, server_default=text("now()"))
    ended_at = Column(DateTime, nullable=True)
    source = Column(String)

class Event(Base):
    """Represents a time-ordered event occurring during a call."""

    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True)
    call_id = Column(String, ForeignKey("calls.call_id"))
    type = Column(String)
    payload = Column(JSON)
    created_at = Column(DateTime, server_default=text("now()"))

class LeadSnapshot(Base):
    """Stores the latest extracted and inferred lead information for a call."""

    __tablename__ = "lead_snapshot"

    call_id = Column(String, ForeignKey("calls.call_id"), primary_key=True)
    language = Column(String, default="unknown")
    city_text = Column(String, nullable=True)
    region_value = Column(String, default="unknown")
    region_confirmed = Column(Boolean, nullable=True)
    budget_band = Column(String, default="unknown")
    timeline_bucket = Column(String, default="unknown")
    room_size_text = Column(String, nullable=True)
    email = Column(String, nullable=True)
    qualification_status = Column(String, default="unknown")
    qualification_reasons = Column(JSON, default=list)
    updated_at = Column(DateTime, server_default=text("now()"), onupdate=text("now()"))
