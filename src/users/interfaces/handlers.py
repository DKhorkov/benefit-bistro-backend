from abc import ABC, abstractmethod
from typing import Any

from src.core.interfaces.handlers import AbstractEventHandler, AbstractCommandHandler
from src.core.interfaces.commands import AbstractCommand
from src.core.interfaces.events import AbstractEvent
from src.users.interfaces import UsersUnitOfWork


class UsersEventHandler(AbstractEventHandler, ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    @abstractmethod
    async def __call__(self, event: AbstractEvent) -> None:
        raise NotImplementedError


class UsersCommandHandler(AbstractCommandHandler, ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    @abstractmethod
    async def __call__(self, command: AbstractCommand) -> Any:
        raise NotImplementedError
