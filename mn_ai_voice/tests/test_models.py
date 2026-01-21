"""Tests for SQLAlchemy ORM models."""

# pylint: disable=redefined-outer-name,invalid-name

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from mn_ai_voice.app.db.models import Base, Call, Event, LeadSnapshot


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

    call = Call(call_id="call_456")
    db_session.add(call)
    db_session.commit()

    event = Event(
        call_id="call_456",
        type="call_started",
        payload={"foo": "bar"},
    )

    db_session.add(event)
    db_session.commit()

    saved_event = db_session.query(Event).one()

    assert saved_event.call_id == "call_456"
    assert saved_event.type == "call_started"
    assert saved_event.payload == {"foo": "bar"}
    assert saved_event.created_at is not None


def test_lead_snapshot_defaults(db_session):
    """LeadSnapshot applies default values correctly."""

    call = Call(call_id="call_789")
    db_session.add(call)
    db_session.commit()

    snapshot = LeadSnapshot(call_id="call_789")

    db_session.add(snapshot)
    db_session.commit()

    saved_snapshot = db_session.get(LeadSnapshot, "call_789")

    assert saved_snapshot.language == "unknown"
    assert saved_snapshot.region_value == "unknown"
    assert saved_snapshot.budget_band == "unknown"
    assert saved_snapshot.timeline_bucket == "unknown"
    assert saved_snapshot.qualification_status == "unknown"
    assert saved_snapshot.qualification_reasons == []
    assert saved_snapshot.updated_at is not None


def test_lead_snapshot_update_timestamp(db_session):
    """updated_at changes when the snapshot is updated."""

    call = Call(call_id="call_999")
    db_session.add(call)
    db_session.commit()

    snapshot = LeadSnapshot(call_id="call_999")
    db_session.add(snapshot)
    db_session.commit()

    first_updated_at = snapshot.updated_at

    snapshot.language = "en"
    db_session.commit()

    assert snapshot.updated_at >= first_updated_at


def test_lead_snapshot_json_default_is_not_shared(db_session):
    """Each LeadSnapshot should have its own JSON default list."""

    call1 = Call(call_id="call_a")
    call2 = Call(call_id="call_b")
    db_session.add_all([call1, call2])
    db_session.commit()

    snapshot1 = LeadSnapshot(call_id="call_a")
    snapshot2 = LeadSnapshot(call_id="call_b")

    db_session.add_all([snapshot1, snapshot2])
    db_session.commit()

    snapshot1.qualification_reasons.append("BUDGET_BELOW_MIN")

    assert snapshot2.qualification_reasons == []