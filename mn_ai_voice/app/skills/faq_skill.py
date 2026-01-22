from mn_ai_voice.app.skills.base import Skill
from mn_ai_voice.app.engine.kb_router import KBRouter


class FAQSkill(Skill):
    def __init__(self):
        self.router = KBRouter()

    def can_handle(self, text: str) -> bool:
        return self.router.route(text) is not None

    def handle(self, context):
        return self.router.route(context.text)  # type: ignore
