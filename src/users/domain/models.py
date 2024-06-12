from dataclasses import dataclass

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
