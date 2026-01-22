"""Database session and engine configuration.

Provides SQLAlchemy engine and session factory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mn_ai_voice.app.core.config import settings
from mn_ai_voice.app.db.models import Base  # 👈 add this

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)
