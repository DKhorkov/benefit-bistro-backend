from dataclasses import dataclass

from src.core.interfaces.commands import AbstractCommand


@dataclass(frozen=True)
class RegisterUserCommand(AbstractCommand):
    username: str
    password: str
    email: str


@dataclass(frozen=True)
class VerifyUserCredentialsCommand(AbstractCommand):
    username: str
    password: str


@dataclass(frozen=True)
class VerifyUserEmailCommand(AbstractCommand):
    user_id: int


@dataclass(frozen=True)
class GetUserCommand(AbstractCommand):
    user_id: int
