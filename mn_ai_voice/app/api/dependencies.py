"""API dependencies for FastAPI routes."""

from typing import Generator

from sqlalchemy.orm import Session

from mn_ai_voice.app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Database dependency for FastAPI routes.

    Yields:
        Database session for the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
