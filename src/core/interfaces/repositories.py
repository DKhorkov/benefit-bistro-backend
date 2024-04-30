from abc import ABC, abstractmethod
from typing import Any, List
from pydantic import PositiveInt


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self, model: Any):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: PositiveInt) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: PositiveInt) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: PositiveInt) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[Any]:
        raise NotImplementedError
