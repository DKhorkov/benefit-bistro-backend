from dataclasses import dataclass

from src.core.interfaces.events import AbstractEvent


@dataclass(frozen=True)
class UserRegisteredEvent(AbstractEvent):
    user_id: int
    username: str
    email: str
