"""FAQ skill implementation.

Handles user queries that map to predefined knowledge base entries.
"""

from typing import Any

from mn_ai_voice.app.skills.base import Skill
from mn_ai_voice.app.engine.kb_router import KBRouter


class FAQSkill(Skill):
    """Skill responsible for answering FAQ-style user questions."""

    def __init__(self) -> None:
        self.router = KBRouter()

    def can_handle(self, text: str) -> bool:
        """Return True if the input text can be routed to the knowledge base."""
        return self.router.route(text) is not None

    def handle(self, context: Any) -> str | None:
        """Handle the request by returning a knowledge base response.

        Args:
            context: Execution context containing user input.

        Returns:
            A knowledge base response string if available, otherwise None.
        """
        return self.router.route(context.text)
