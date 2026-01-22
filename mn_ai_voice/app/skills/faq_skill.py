"""
FAQ skill implementation.

Handles user queries that map to predefined knowledge base entries.
"""

from dataclasses import dataclass

from mn_ai_voice.app.skills.base import Skill
from mn_ai_voice.app.engine.kb_router import KBRouter


@dataclass
class FAQContext:
    """Context object containing user input text for FAQ processing."""
    text: str


class FAQSkill(Skill):
    """Skill responsible for answering FAQ-style user questions."""

    def __init__(self) -> None:
        self.router = KBRouter()

    def can_handle(self, text: str) -> bool:
        """Return True if the input text can be routed to the knowledge base."""
        return self.router.route(text) is not None

    def handle(self, context: FAQContext) -> str | None:
        """Handle the request by returning a knowledge base response."""
        return self.router.route(context.text)
