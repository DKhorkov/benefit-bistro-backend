from abc import abstractmethod
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces import AbstractRepository, BaseModel


class SQLAlchemyRepository(AbstractRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    @abstractmethod
    async def add(self, model: BaseModel) -> None:
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
