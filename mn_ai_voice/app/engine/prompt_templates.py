"""
Prompt templates for conversation flow.

Maps conversation states to user-facing prompt strings.
"""

from mn_ai_voice.app.core.constants import CallState


class PromptRenderer:
    """Renders user prompts based on the current conversation state."""

    _prompts = {
        CallState.ASK_LANGUAGE: "Would you like to speak in English, Hindi, or Hinglish?",
        CallState.ASK_CITY_OR_REGION: "Which city are you in?",
        CallState.ASK_REGION_CONFIRM: "Is your city in South India, Maharashtra, or Delhi/NCR?",
        CallState.ASK_TIMELINE: "When are you planning to start?",
        CallState.ASK_BUDGET: "A full kids room typically costs ₹6–₹9 lakhs. Does that work?",
        CallState.ASK_ROOM_SIZE: "What is the room size?",
        CallState.ASK_EMAIL: "Please share your email for consultation details.",
        CallState.CLOSE: "Thanks! You’ll receive the details shortly.",
    }

    def render(self, state: CallState) -> str:
        """Return the prompt string for the given conversation state."""
        if state not in self._prompts:
            raise ValueError(f"No prompt defined for CallState: {state}")
        return self._prompts[state]
