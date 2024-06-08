from abc import ABC, abstractmethod
from typing import Self, List

from src.core.interfaces.events import AbstractEvent


class AbstractUnitOfWork(ABC):
    """
    Interface for any units of work, which would be used for transaction atomicity, according DDD.
    """

    def __init__(self):
        # Creating events storage for retrieve them in MessageBus:
        self.events: List[AbstractEvent] = []

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
