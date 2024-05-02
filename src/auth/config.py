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


class CookiesConfig(BaseSettings):
    COOKIES_KEY: str
    COOKIES_LIFESPAN_DAYS: int
    SECURE_COOKIES: bool
    HTTP_ONLY: bool
    SAME_SITE: str


class PasslibConfig(BaseSettings):
    PASSLIB_SCHEME: str
    PASSLIB_DEPRECATED: str


jwt_config: JWTConfig = JWTConfig()
cookies_config: CookiesConfig = CookiesConfig()
passlib_config: PasslibConfig = PasslibConfig()
