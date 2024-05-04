from typing import Self
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.core.interfaces import AbstractUnitOfWork
from src.core.database.connection import session_factory as default_session_factory


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory: async_sessionmaker = default_session_factory) -> None:
        self._session_factory: async_sessionmaker = session_factory

    async def __aenter__(self) -> Self:
        self._session: AsyncSession = self._session_factory()
        return await super().__aenter__()

    async def __aexit__(self, *args, **kwargs) -> None:
        await super().__aexit__(*args, **kwargs)
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
