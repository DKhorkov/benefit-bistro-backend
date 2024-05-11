from dataclasses import dataclass
from typing import Tuple, List, Literal
from enum import Enum
from pydantic_settings import BaseSettings

from src.config import (
    PageNamesConfig as BasePageNamesConfig,
    PathsConfig as BasePathsConfig
)


@dataclass(frozen=True)
class PageNamesConfig(BasePageNamesConfig):
    REGISTER_PAGE: str = BasePageNamesConfig.HOMEPAGE
    LOGIN_PAGE: str = BasePageNamesConfig.HOMEPAGE
    EMAIL_VERIFIED: str = BasePageNamesConfig.HOMEPAGE


@dataclass(frozen=True)
class PathsConfig(BasePathsConfig):
    REGISTER_PAGE: str = 'register.html'
    LOGIN_PAGE: str = 'login.html'
    EMAIL_VERIFIED: str = 'email_verified.html'


@dataclass(frozen=True)
class URLPathsConfig:
    REGISTER_PAGE: str = '/register_page'
    LOGIN_PAGE: str = '/login_page'
    REGISTER: str = '/register'
    LOGIN: str = '/login'
    LOGOUT: str = '/logout'
    ME: str = '/me'
    VERIFY_EMAIL: str = '/verify_email/{token}'
    EMAIL_VERIFIED: str = '/email_verified'


@dataclass(frozen=True)
class URLNamesConfig:
    REGISTER_PAGE: str = 'register_page'
    LOGIN_PAGE: str = 'login_page'
    REGISTER: str = 'register'
    LOGIN: str = 'login'
    LOGOUT: str = 'logout'
    ME: str = 'me'
    VERIFY_EMAIL: str = 'verify_email'
    EMAIL_VERIFIED: str = 'email_verified'


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


class CookiesConfig(BaseSettings):
    COOKIES_KEY: str
    COOKIES_LIFESPAN_DAYS: int
    SECURE_COOKIES: bool
    HTTP_ONLY: bool
    SAME_SITE: Literal['strict', 'lax', 'none']


class PasslibConfig(BaseSettings):
    PASSLIB_SCHEME: str
    PASSLIB_DEPRECATED: str


cookies_config: CookiesConfig = CookiesConfig()
passlib_config: PasslibConfig = PasslibConfig()
