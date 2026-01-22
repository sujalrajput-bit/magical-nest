"""Base skill abstraction.

Defines the interface for conversational skills that can
inspect and handle user input.
"""

from abc import ABC, abstractmethod
from typing import Any


class Skill(ABC):
    """Abstract base class for all conversational skills."""

    @abstractmethod
    def can_handle(self, text: str) -> bool:
        """Return True if this skill can handle the given user input."""

    @abstractmethod
    def handle(self, context: Any) -> Any:
        """Handle the request using the provided execution context."""
