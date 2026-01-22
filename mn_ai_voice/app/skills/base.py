from abc import ABC, abstractmethod


class Skill(ABC):
    @abstractmethod
    def can_handle(self, text: str) -> bool:
        pass

    @abstractmethod
    def handle(self, context):
        pass
