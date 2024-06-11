from abc import ABC, abstractmethod
from typing import Any

from src.core.interfaces.handlers import AbstractEventHandler, AbstractCommandHandler
from src.core.interfaces.commands import AbstractCommand
from src.core.interfaces.events import AbstractEvent
from src.groups.interfaces.units_of_work import GroupsUnitOfWork


class GroupEventHandler(AbstractEventHandler, ABC):
    """
    Abstract event handler class, from every event handler should be inherited from.
    """

    def __init__(self, uow: GroupsUnitOfWork) -> None:
        self._uow: GroupsUnitOfWork = uow

    @abstractmethod
    async def __call__(self, event: AbstractEvent) -> None:
        raise NotImplementedError


class GroupCommandHandler(AbstractCommandHandler, ABC):
    """
    Abstract command handler class, from every command handler should be inherited from.
    """

    def __init__(self, uow: GroupsUnitOfWork) -> None:
        self._uow: GroupsUnitOfWork = uow

    @abstractmethod
    async def __call__(self, command: AbstractCommand) -> Any:
        raise NotImplementedError
