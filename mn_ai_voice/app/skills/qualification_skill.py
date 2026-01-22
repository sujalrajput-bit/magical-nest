"""
Qualification skill logic.

Applies extraction and qualification rules to update a lead snapshot
based on user input, independent of strict conversation order.
"""

from typing import Any

from mn_ai_voice.app.engine.extractors import BudgetExtractor, EmailExtractor
from mn_ai_voice.app.engine.qualification_rules import QualificationService
from mn_ai_voice.app.core.constants import CallState


class QualificationSkill:
    """Skill responsible for extracting and evaluating lead qualification data."""

    def __init__(self) -> None:
        self.budget_extractor = BudgetExtractor()
        self.email_extractor = EmailExtractor()
        self.qualifier = QualificationService()

    def apply(self, state: CallState, text: str, snapshot: Any) -> Any:
        """
        Apply qualification-related logic based on user input.

        - Extract budget whenever mentioned
        - Extract email only when explicitly asked
        - Evaluate qualification once sufficient data exists
        """

        # --- Budget extraction (can happen anytime) ---
        budget_band = self.budget_extractor.extract(text)
        if budget_band != "unknown":
            snapshot.budget_band = budget_band

        # --- Email extraction (only when asked) ---
        if state == CallState.ASK_EMAIL:
            email = self.email_extractor.extract(text)
            if email:
                snapshot.email = email

        # --- Qualification evaluation (run once when ready) ---
        if (
            snapshot.qualification_status in (None, "unknown")
            and snapshot.region_value not in (None, "unknown")
            and snapshot.budget_band not in (None, "unknown")
        ):
            status, reasons = self.qualifier.evaluate(
                snapshot.region_value,
                snapshot.budget_band,
            )
            snapshot.qualification_status = status.value
            snapshot.qualification_reasons = [r.value for r in reasons]

        return snapshot
