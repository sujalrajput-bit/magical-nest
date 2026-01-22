"""
Deterministic extractors for converting user text
into structured fields.

Pure logic. No DB. No framework.
"""

import re
from typing import Optional


class LanguageExtractor:
    """Detect preferred language from user input."""

    def extract(self, text: str) -> str:
        """
        Extract the preferred language from user input text.

        Args:
            text: User input text to analyze for language preference.

        Returns:
            Language code: "hindi", "hinglish", "english", or "unknown".
        """
        t = text.lower()

        if any(word in t for word in ["hindi", "हिंदी"]):
            return "hindi"

        if any(word in t for word in ["hinglish", "mix"]):
            return "hinglish"

        if any(word in t for word in ["english", "eng"]):
            return "english"

        return "unknown"


class RegionExtractor:
    """Detect serviceable region from city/state mentions."""

    SOUTH_INDIA_STATES = {
        "karnataka", "ka", "tamil nadu", "tn", "telangana", "tg", "andhra", "ap", "kerala", "kl"
    }
    MAHARASHTRA = {"maharashtra", "mh", "pune", "mumbai", "nagpur"}
    DELHI_NCR = {
        "delhi", "ncr", "gurgaon", "gurugram", "noida", "ghaziabad"
    }

    def extract(self, text: str) -> str:
        """
        Extract the serviceable region from user input text.

        Args:
            text: User input text to analyze for region mentions.

        Returns:
            Region code: "south_india", "maharashtra", "delhi_ncr", or "unknown".
        """
        t = text.lower()

        if any(k in t for k in self.SOUTH_INDIA_STATES):
            return "south_india"

        if any(k in t for k in self.MAHARASHTRA):
            return "maharashtra"

        if any(k in t for k in self.DELHI_NCR):
            return "delhi_ncr"

        return "unknown"


class BudgetExtractor:
    """Extract budget band from text (in lakhs)."""

    def extract(self, text: str) -> str:
        """
        Extract budget band from text by finding numeric values.

        Args:
            text: User input text containing budget information.

        Returns:
            Budget band: "below_6L", "6_to_9L", "above_9L", or "unknown".
        """
        match = re.search(r"(\d+(\.\d+)?)", text)
        if not match:
            return "unknown"

        value = float(match.group(1))

        if value < 6:
            return "below_6L"
        if 6 <= value <= 9:
            return "6_to_9L"
        return "above_9L"


class TimelineExtractor:
    """Bucket timeline intent."""

    def extract(self, text: str) -> str:
        """
        Extract timeline intent from user input text.

        Args:
            text: User input text to analyze for timeline preferences.

        Returns:
            Timeline bucket: "immediate", "1_month", "2_3_months", "3_plus", or "unknown".
        """
        t = text.lower()

        if any(k in t for k in ["immediate", "asap", "now"]):
            return "immediate"

        if "1 month" in t or "one month" in t:
            return "1_month"

        if any(k in t for k in ["2 months", "3 months", "2-3", "2 to 3"]):
            return "2_3_months"

        if any(k in t for k in ["later", "next year", "3+"]):
            return "3_plus"

        return "unknown"


class EmailExtractor:
    """Extract email using regex."""

    def extract(self, text: str) -> Optional[str]:
        """
        Extract the first email address found in the text.

        Args:
            text: User input text to search for email addresses.

        Returns:
            The first email address found, or None if no email is found.
        """
        match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        return match.group(0) if match else None


class RoomSizeExtractor:
    """Store room size as raw text."""

    def extract(self, text: str) -> str:
        """
        Extract room size information as raw text.

        Args:
            text: User input text containing room size information.

        Returns:
            The input text with leading and trailing whitespace removed.
        """
        return text.strip()
