from dataclasses import dataclass
from typing import Tuple, List, Literal
from enum import Enum

from pydantic_settings import BaseSettings


@dataclass(frozen=True)
class URLPathsConfig:
    REGISTER_PAGE: str = '/register_page'
    LOGIN_PAGE: str = '/login_page'
    REGISTER: str = '/register'
    LOGIN: str = '/login'
    LOGOUT: str = '/logout'


@dataclass(frozen=True)
class URLNamesConfig:
    REGISTER_PAGE: str = 'register_page'
    LOGIN_PAGE: str = 'login_page'
    REGISTER: str = 'register'
    LOGIN: str = 'login'
    LOGOUT: str = 'logout'


@dataclass(frozen=True)
class UserValidationConfig:
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 30
    USERNAME_MIN_LENGTH: int = 5
    USERNAME_MAX_LENGTH: int = 20


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
    SAME_SITE: Literal['strict', 'lax', 'none']


class PasslibConfig(BaseSettings):
    PASSLIB_SCHEME: str
    PASSLIB_DEPRECATED: str


jwt_config: JWTConfig = JWTConfig()
cookies_config: CookiesConfig = CookiesConfig()
passlib_config: PasslibConfig = PasslibConfig()
