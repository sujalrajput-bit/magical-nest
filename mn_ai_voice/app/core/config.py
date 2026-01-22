"""
Application configuration and environment settings.
"""

from pathlib import Path

import yaml  # type: ignore[import]
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/mn_ai_voice"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()


# ---------- Knowledge Base Loader (Week-1) ----------

BASE_DIR = Path(__file__).resolve().parent.parent
KB_PATH = BASE_DIR / "knowledge" / "knowledge_base.yaml"


def load_knowledge_base():
    """
    Load the knowledge base from YAML file or return default FAQ data.

    Returns:
        dict: Knowledge base data containing FAQ information. If the knowledge
        base YAML file exists, it loads the data from that file. Otherwise,
        returns a default dictionary with basic process information.
    """
    if not KB_PATH.exists():
        return {
            "faq": {
                "process": "Our process includes a design consultation, "
                "3D designs, and turnkey execution."
            }
        }

    with open(KB_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


KNOWLEDGE_BASE = load_knowledge_base()
