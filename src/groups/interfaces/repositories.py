from typing import Optional, List
from abc import ABC, abstractmethod

from src.core.interfaces import AbstractRepository, AbstractModel
from src.groups.models import GroupModel


class GroupsRepository(AbstractRepository, ABC):
    """
    An interface for work with groups, that is used by groups unit of work of the groups' module.
    The main goal is that implementations of this interface can be easily replaced in the groups unit of work of
    the groups module using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_owner_and_name(self, name: str, owner_id: int) -> Optional[GroupModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_owner_groups(self, owner_id: int) -> List[GroupModel]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: AbstractModel) -> GroupModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[GroupModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: AbstractModel) -> GroupModel:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[GroupModel]:
        raise NotImplementedError
