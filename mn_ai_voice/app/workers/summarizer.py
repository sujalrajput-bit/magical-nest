"""
Call summarizer worker.

Generates a call summary artifact at call end
and enqueues a CRM note via the outbox.

This worker is idempotent and safe to retry.
"""

from sqlalchemy.orm import Session

from mn_ai_voice.app.db.models import (
    Call,
    Lead,
    LeadSnapshot,
    Artifact,
    CRMOutbox,
)


class CallSummarizer:
    """Generates summary artifacts and CRM notes for completed calls."""

    def run(self, db: Session, call_id: str) -> None:
        """
        Generate call summary and enqueue CRM note.

        This method is idempotent:
        - Summary artifact is created only once
        - CRM outbox entry is protected by idempotency key
        """

        call = db.get(Call, call_id)
        if call is None or call.ended_at is None:
            # Only summarize completed calls
            return

        lead = db.get(Lead, call.lead_id)
        snapshot = db.get(LeadSnapshot, call.lead_id)

        if lead is None or snapshot is None:
            return

        # 1 Create summary artifact (idempotent)
        existing_artifact = (
            db.query(Artifact)
            .filter(
                Artifact.call_id == call_id,
                Artifact.type == "summary",
            )
            .one_or_none()
        )

        if existing_artifact is None:
            artifact = Artifact(
                call_id=call_id,
                type="summary",
                content_text=self._build_summary_text(
                    lead=lead,
                    snapshot=snapshot,
                ),
            )
            db.add(artifact)

        # 2 Enqueue CRM note (idempotent)
        idempotency_key = f"crm_note:{call_id}"

        existing_outbox = (
            db.query(CRMOutbox)
            .filter(CRMOutbox.idempotency_key == idempotency_key)
            .one_or_none()
        )

        if existing_outbox is None:
            db.add(
                CRMOutbox(
                    call_id=call_id,
                    action="append_note",
                    payload={
                        "lead_phone": lead.primary_phone,
                        "summary": self._build_summary_payload(snapshot),
                    },
                    idempotency_key=idempotency_key,
                )
            )

        db.commit()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_summary_text(self, lead: Lead, snapshot: LeadSnapshot) -> str:
        """Generate human-readable call summary text."""

        lines = [
            f"Phone: {lead.primary_phone}",
            f"Region: {snapshot.region_value or 'unknown'}",
            f"City: {snapshot.city_text or 'unknown'}",
            f"Budget: {snapshot.budget_band or 'unknown'}",
            f"Timeline: {snapshot.timeline_bucket or 'unknown'}",
            f"Room size: {snapshot.room_size_text or 'unknown'}",
            f"Qualification: {snapshot.qualification_status or 'unknown'}",
        ]

        if snapshot.email:
            lines.append(f"Email: {snapshot.email}")

        if snapshot.qualification_reasons:
            lines.append(
                f"Reasons: {', '.join(snapshot.qualification_reasons)}"
            )

        return "\n".join(lines)

    def _build_summary_payload(self, snapshot: LeadSnapshot) -> dict:
        """Generate structured summary payload for CRM."""

        return {
            "region": snapshot.region_value,
            "budget_band": snapshot.budget_band,
            "timeline": snapshot.timeline_bucket,
            "room_size": snapshot.room_size_text,
            "qualification_status": snapshot.qualification_status,
            "qualification_reasons": snapshot.qualification_reasons,
            "email": snapshot.email,
        }
