"""
Tests for SQLAlchemy ORM models.
"""

# pylint: disable=redefined-outer-name,invalid-name

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from mn_ai_voice.app.db.models import Base, Call, Event, Lead, LeadSnapshot


@pytest.fixture()
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")

    # Enable foreign key constraints in SQLite
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
    finally:
        session.close()


def test_create_call(db_session):
    """Call model can be created and persisted."""

    call = Call(
        call_id="call_123",
        from_phone="+919999999999",
        status="in_progress",
        current_state="ASK_LANGUAGE",
        source="exotel",
    )

    db_session.add(call)
    db_session.commit()

    saved_call = db_session.get(Call, "call_123")

    assert saved_call is not None
    assert saved_call.call_id == "call_123"
    assert saved_call.status == "in_progress"
    assert saved_call.current_state == "ASK_LANGUAGE"
    assert saved_call.started_at is not None
    assert saved_call.ended_at is None


def test_create_event_for_call(db_session):
    """Event can be created for an existing call."""

    call = Call(
        call_id="call_456",
        direction="inbound",
        status="in_progress",
        current_state="ASK_LANGUAGE",
    )
    db_session.add(call)
    db_session.commit()

    event = Event(
        call_id="call_456",
        type="call_started",
        payload_json={"foo": "bar"},
    )

    db_session.add(event)
    db_session.commit()

    assert event.event_id is not None

def test_lead_snapshot_defaults(db_session):
    """LeadSnapshot applies default values correctly."""

    lead = Lead(
        lead_id="l_789",
        primary_phone="+911111111111",
    )
    db_session.add(lead)
    db_session.flush()

    call = Call(
        call_id="call_789",
        lead_id=lead.lead_id,
    )
    db_session.add(call)
    db_session.commit()

    snapshot = LeadSnapshot(lead_id=lead.lead_id)
    db_session.add(snapshot)
    db_session.commit()

    assert snapshot.language == "unknown"
    assert snapshot.region_value == "unknown"
    assert snapshot.budget_band == "unknown"
    assert snapshot.qualification_status == "unknown"


def test_lead_snapshot_update_timestamp(db_session):
    """updated_at changes when the snapshot is updated."""

    lead = Lead(
        lead_id="l_999",
        primary_phone="+922222222222",
    )
    db_session.add(lead)
    db_session.flush()

    call = Call(
        call_id="call_999",
        lead_id=lead.lead_id,
    )
    db_session.add(call)
    db_session.commit()

    snapshot = LeadSnapshot(lead_id=lead.lead_id)
    db_session.add(snapshot)
    db_session.commit()

    old_updated_at = snapshot.updated_at

    snapshot.budget_band = "6_to_9L"
    db_session.commit()

    assert snapshot.updated_at > old_updated_at


def test_lead_snapshot_json_default_is_not_shared(db_session):
    """Each LeadSnapshot should have its own JSON default list."""

    lead1 = Lead(
        lead_id="l_a",
        primary_phone="+933333333333",
    )
    lead2 = Lead(
        lead_id="l_b",
        primary_phone="+944444444444",
    )
    db_session.add_all([lead1, lead2])
    db_session.flush()

    call1 = Call(call_id="call_a", lead_id=lead1.lead_id)
    call2 = Call(call_id="call_b", lead_id=lead2.lead_id)
    db_session.add_all([call1, call2])
    db_session.commit()

    snapshot1 = LeadSnapshot(lead_id=lead1.lead_id)
    snapshot2 = LeadSnapshot(lead_id=lead2.lead_id)
    db_session.add_all([snapshot1, snapshot2])
    db_session.commit()

    snapshot1.qualification_reasons.append("BUDGET_LOW")

    assert snapshot2.qualification_reasons == []
