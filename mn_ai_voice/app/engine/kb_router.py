from mn_ai_voice.app.core.config import KNOWLEDGE_BASE


class KBRouter:
    def route(self, text: str) -> str | None:
        text = text.lower()
        if "process" in text:
            return KNOWLEDGE_BASE["faq"]["process"]
        return None
