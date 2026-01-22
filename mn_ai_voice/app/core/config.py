"""
Application configuration and environment settings.
"""

import yaml
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    DATABASE_URL: str = "sqlite:///./local.db"  # default for Week-1 local dev

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()  # type: ignore[call-arg]


# ---------- Knowledge Base Loader (Week-1) ----------

BASE_DIR = Path(__file__).resolve().parent.parent
KB_PATH = BASE_DIR / "knowledge" / "knowledge_base.yaml"


def load_knowledge_base():
    if not KB_PATH.exists():
        return {
            "faq": {
                "process": "Our process includes a design consultation, 3D designs, and turnkey execution."
            }
        }

    with open(KB_PATH, "r") as f:
        return yaml.safe_load(f)


KNOWLEDGE_BASE = load_knowledge_base()
