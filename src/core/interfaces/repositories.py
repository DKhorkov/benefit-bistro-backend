from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.interfaces.base_model import BaseModel


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self, model: BaseModel):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[BaseModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: BaseModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[BaseModel]:
        raise NotImplementedError
