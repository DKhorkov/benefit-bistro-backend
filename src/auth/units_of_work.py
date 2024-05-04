from typing import Self

from src.auth.repositories import UsersRepository
from src.core.database.units_of_work import SQLAlchemyUnitOfWork


class UsersUnitOfWork(SQLAlchemyUnitOfWork):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users: UsersRepository = UsersRepository(session=self._session)
        return uow
