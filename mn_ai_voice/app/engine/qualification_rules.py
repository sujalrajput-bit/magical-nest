
"""Lead qualification evaluation logic.

Determines whether a lead is qualified, nurtured, or unqualified
based on region and budget band.
"""

from typing import List, Tuple

from mn_ai_voice.app.core.constants import (
    QualificationStatus,
    QualificationReason,
)


class QualificationService:
    """Evaluates lead qualification based on business rules."""

    def evaluate(
        self,
        region: str,
        budget_band: str,
    ) -> Tuple[QualificationStatus, List[QualificationReason]]:
        """Evaluate a lead and return its qualification status and reasons.

        Args:
            region: Normalized region identifier (e.g. south_india).
            budget_band: Normalized budget band (e.g. below_6L, 6_to_9L).

        Returns:
            A tuple of:
            - QualificationStatus
            - List of QualificationReason explaining the decision
        """
        if region not in {"south_india", "maharashtra", "delhi_ncr"}:
            return (
                QualificationStatus.UNQUALIFIED,
                [QualificationReason.REGION_NOT_SERVED],
            )

        if budget_band == "below_6L":
            return (
                QualificationStatus.NURTURE,
                [QualificationReason.BUDGET_BELOW_MIN],
            )

        reasons: List[QualificationReason] = []
        if budget_band == "above_9L":
            reasons.append(QualificationReason.BUDGET_ABOVE_BAND)

        return QualificationStatus.QUALIFIED, reasons
