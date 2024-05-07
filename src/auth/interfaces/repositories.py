from typing import Optional
from abc import ABC, abstractmethod
from src.core.interfaces import BaseModel, AbstractRepository


class UsersRepository(AbstractRepository, ABC):
    """
    An interface for work with users, that is used by users unit of work of the authorization module.
    The main goal is that implementations of this interface can be easily replaced in the users unit of work of
    the authorization module using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[BaseModel]:
        raise NotImplementedError
