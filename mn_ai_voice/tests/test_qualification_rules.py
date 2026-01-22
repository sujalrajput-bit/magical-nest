"""
Unit tests for lead qualification rules.

These tests validate business logic for:
- Region serviceability
- Budget qualification bands
"""

from mn_ai_voice.app.engine.qualification_rules import QualificationService
from mn_ai_voice.app.core.constants import (
    QualificationStatus,
    QualificationReason,
)


def test_qualified_above_band():
    """
    Region served + budget above ₹9L
    → QUALIFIED with BUDGET_ABOVE_BAND reason
    """
    service = QualificationService()

    status, reasons = service.evaluate(
        region="maharashtra",
        budget_band="above_9L",
    )

    assert status == QualificationStatus.QUALIFIED
    assert QualificationReason.BUDGET_ABOVE_BAND in reasons


def test_nurture_below_min_budget():
    """
    Region served + budget below ₹6L
    → NURTURE with BUDGET_BELOW_MIN reason
    """
    service = QualificationService()

    status, reasons = service.evaluate(
        region="south_india",
        budget_band="below_6L",
    )

    assert status == QualificationStatus.NURTURE
    assert QualificationReason.BUDGET_BELOW_MIN in reasons


def test_unqualified_region_not_served():
    """
    Region not served (outside South India / MH / Delhi NCR)
    → UNQUALIFIED with REGION_NOT_SERVED reason
    """
    service = QualificationService()

    status, reasons = service.evaluate(
        region="europe",
        budget_band="6_to_9L",
    )

    assert status == QualificationStatus.UNQUALIFIED
    assert QualificationReason.REGION_NOT_SERVED in reasons


def test_qualified_within_band_no_reasons():
    """
    Region served + budget within ₹6–₹9L
    → QUALIFIED with no reasons
    """
    service = QualificationService()

    status, reasons = service.evaluate(
        region="delhi_ncr",
        budget_band="6_to_9L",
    )

    assert status == QualificationStatus.QUALIFIED
    assert not reasons
