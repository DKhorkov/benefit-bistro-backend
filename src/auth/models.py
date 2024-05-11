from dataclasses import dataclass

from src.core.interfaces import BaseModel


@dataclass
class UserModel(BaseModel):
    email: str
    password: str
    username: str

    # Optional args:
    id: int = 0
    email_verified: bool = False
