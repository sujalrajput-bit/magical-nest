"""Qualification skill logic.

Applies extraction and qualification rules to update a lead snapshot
based on the current conversation state and user input.
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
        """Apply qualification-related logic based on the current call state.

        Args:
            state: Current conversation state.
            text: Raw user input text.
            snapshot: Mutable lead snapshot object to update.

        Returns:
            The updated lead snapshot.
        """
        if state == CallState.ASK_BUDGET:
            snapshot.budget_band = self.budget_extractor.extract(text)

        if state == CallState.ASK_EMAIL:
            snapshot.email = self.email_extractor.extract(text)

        if state == CallState.QUALIFY:
            status, reasons = self.qualifier.evaluate(
                snapshot.region_value,
                snapshot.budget_band,
            )
            snapshot.qualification_status = status.value
            snapshot.qualification_reasons = [r.value for r in reasons]

        return snapshot
