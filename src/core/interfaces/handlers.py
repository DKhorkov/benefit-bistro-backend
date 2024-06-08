from abc import ABC, abstractmethod

from src.core.interfaces import AbstractUnitOfWork
from src.core.interfaces.commands import AbstractCommand
from src.core.interfaces.events import AbstractEvent


class AbstractEventHandler(ABC):

    @abstractmethod
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, event: AbstractEvent) -> None:
        raise NotImplementedError


class AbstractCommandHandler(ABC):

    @abstractmethod
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        raise NotImplementedError

    @abstractmethod
    async def __call__(self, command: AbstractCommand) -> None:
        raise NotImplementedError
