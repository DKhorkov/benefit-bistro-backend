from dataclasses import dataclass
from pydantic_settings import BaseSettings
from typing import List


@dataclass(frozen=True)
class PathsConfig:
    TEMPLATES: str = 'templates/'
    STATIC: str = 'static/'
    HOMEPAGE: str = 'homepage.html'


@dataclass(frozen=True)
class PageNamesConfig:
    HOMEPAGE: str = 'Benefit Bistro'


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


class LinksConfig(BaseSettings):
    HTTP_PROTOCOL: str
    DOMAIN: str


cors_config: CORSConfig = CORSConfig()
uvicorn_config: UvicornConfig = UvicornConfig()
links_config: LinksConfig = LinksConfig()
