from mn_ai_voice.app.engine.extractors import BudgetExtractor, EmailExtractor
from mn_ai_voice.app.engine.qualification_rules import QualificationService
from mn_ai_voice.app.core.constants import CallState


class QualificationSkill:
    def __init__(self):
        self.budget_extractor = BudgetExtractor()
        self.email_extractor = EmailExtractor()
        self.qualifier = QualificationService()

    def apply(self, state, text, snapshot):
        if state == CallState.ASK_BUDGET:
            snapshot.budget_band = self.budget_extractor.extract(text)

        if state == CallState.ASK_EMAIL:
            snapshot.email = self.email_extractor.extract(text)

        if state == CallState.QUALIFY:
            status, reasons = self.qualifier.evaluate(
                snapshot.region_value, snapshot.budget_band
            )
            snapshot.qualification_status = status.value
            snapshot.qualification_reasons = [r.value for r in reasons]

        return snapshot
