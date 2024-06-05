from dataclasses import dataclass
from typing import Tuple

from src.config import RouterConfig as BaseRouterConfig


@dataclass(frozen=True)
class URLPathsConfig:
    MY_GROUPS: str = '/my'
    CREATE_GROUP: str = ''
    DELETE_GROUP: str = '/{group_id}'
    UPDATE_GROUP_MEMBERS: str = '/{group_id}/members'
    UPDATE_GROUP: str = '/{group_id}'


@dataclass(frozen=True)
class URLNamesConfig:
    MY_GROUPS: str = 'get my groups'
    CREATE_GROUP: str = 'create group'
    DELETE_GROUP: str = 'delete group'
    UPDATE_GROUP_MEMBERS: str = 'update group members'
    UPDATE_GROUP: str = 'update group info'


@dataclass(frozen=True)
class GroupValidationConfig:
    NAME_MIN_LENGTH: int = 1
    NAME_MAX_LENGTH: int = 70


@dataclass(frozen=True)
class RouterConfig(BaseRouterConfig):
    PREFIX: str = '/groups'
    TAGS: Tuple[str] = ('Groups', )
