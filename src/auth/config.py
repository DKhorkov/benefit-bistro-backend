from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum

from pydantic_settings import BaseSettings


@dataclass(frozen=True)
class URLPathsConfig:
    REGISTER: str = '/register'
    LOGIN: str = '/login'
    TOKEN: str = '/token'


@dataclass(frozen=True)
class URLNamesConfig:
    REGISTER: str = 'register'
    LOGIN: str = 'login'
    TOKEN: str = 'token'


@dataclass(frozen=True)
class PasswordConfig:
    MIN_LENGTH: int = 8
    MAX_LENGTH: int = 30


@dataclass(frozen=True)
class RouterConfig:
    PREFIX: str = '/auth'
    TAGS: Tuple[str] = ('Auth', )

    @classmethod
    def tags_list(cls) -> List[str | Enum]:
        return [tag for tag in cls.TAGS]


class JWTConfig(BaseSettings):
    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


jwt_config = JWTConfig()
