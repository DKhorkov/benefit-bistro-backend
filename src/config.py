from pathlib import Path
from dataclasses import dataclass
from pydantic_settings import BaseSettings
from typing import List


@dataclass(frozen=True)
class PathsConfig:
    TEMPLATES: Path = Path('./templates')
    STATIC: Path = Path('./static')

    HOMEPAGE: Path = Path('homepage.html')
    REGISTER_PAGE = Path('register.html')
    LOGIN_PAGE = Path('login.html')


@dataclass(frozen=True)
class PageNamesConfig:
    HOMEPAGE: str = 'Benefit Bistro'
    REGISTER_PAGE: str = HOMEPAGE
    LOGIN_PAGE: str = HOMEPAGE


@dataclass(frozen=True)
class URLPathsConfig:
    HOMEPAGE: str = '/'
    STATIC: str = '/static'


@dataclass(frozen=True)
class URLNamesConfig:
    HOMEPAGE: str = 'homepage'
    STATIC: str = 'static'


class CORSConfig(BaseSettings):
    ALLOW_ORIGINS: List[str]
    ALLOW_HEADERS: List[str]
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: List[str]


class UvicornConfig(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    LOG_LEVEL: str = 'info'
    RELOAD: bool = True


cors_config = CORSConfig()
uvicorn_config = UvicornConfig()
