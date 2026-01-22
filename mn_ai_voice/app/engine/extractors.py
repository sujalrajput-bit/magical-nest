"""Lightweight text extractors for user input.

Provides simple regex-based extractors for budget and email information.
"""

import re

class BudgetExtractor:
    """Extracts and classifies budget information from user text."""

    def extract(self, text: str) -> str:
        """Return a budget band extracted from the given text.

        Returns:
            - "below_6L"
            - "6_to_9L"
            - "above_9L"
            - "unknown" if no budget is found
        """
        match = re.search(r"(\d+)", text)
        if not match:
            return "unknown"

        value = int(match.group(1))
        if value < 6:
            return "below_6L"
        if value <= 9:
            return "6_to_9L"
        return "above_9L"

class EmailExtractor:
    """Extracts an email address from user-provided text."""

    def extract(self, text: str) -> str | None:
        """Return the first email address found in the text, if any."""
        match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        return match.group(0) if match else None
