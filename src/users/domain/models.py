from dataclasses import dataclass
from typing import Any

from src.core.interfaces import AbstractModel


@dataclass
class UserModel(AbstractModel):
    email: str
    password: str
    username: str

    # Optional args:
    id: int = 0
    email_verified: bool = False

    async def protect_password(self) -> None:
        self.password = ''

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)
