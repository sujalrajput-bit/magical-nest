"""Knowledge base routing logic.

Routes user input to predefined knowledge base responses
using simple keyword-based matching.
"""

from mn_ai_voice.app.core.config import KNOWLEDGE_BASE


class KBRouter:
    """Routes user input text to relevant knowledge base entries."""

    def route(self, text: str) -> str | None:
        """Return a knowledge base response for the given text, if any.

        Args:
            text: Raw user input text.

        Returns:
            A knowledge base response string if a match is found,
            otherwise None.
        """
        normalized = text.lower()
        if "process" in normalized:
            return KNOWLEDGE_BASE["faq"]["process"]

        return None
