from dataclasses import dataclass
from typing import Tuple

from src.config import RouterConfig as BaseRouterConfig


@dataclass(frozen=True)
class URLPathsConfig:
    MY_GROUPS: str = '/my_groups'
    CREATE_GROUP: str = '/create'
    DELETE_GROUP: str = '/{group_id}/delete'
    UPDATE_GROUP_MEMBERS: str = '/{group_id}/members/update'


@dataclass(frozen=True)
class URLNamesConfig:
    MY_GROUPS: str = 'my_groups'
    CREATE_GROUP: str = 'create_group'
    DELETE_GROUP: str = 'delete_group'
    UPDATE_GROUP_MEMBERS: str = 'update_group_members'


@dataclass(frozen=True)
class GroupValidationConfig:
    NAME_MIN_LENGTH: int = 1
    NAME_MAX_LENGTH: int = 70


@dataclass(frozen=True)
class RouterConfig(BaseRouterConfig):
    PREFIX: str = '/groups'
    TAGS: Tuple[str] = ('Groups', )
