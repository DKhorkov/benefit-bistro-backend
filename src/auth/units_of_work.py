from typing import Self

from src.auth.interfaces.repositories import UsersRepository
from src.auth.interfaces.units_of_work import UsersUnitOfWork
from src.auth.repositories import SQLAlchemyUsersRepository
from src.core.database.units_of_work import SQLAlchemyUnitOfWork


class SQLAlchemyUsersUnitOfWork(SQLAlchemyUnitOfWork, UsersUnitOfWork):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.users: UsersRepository = SQLAlchemyUsersRepository(session=self._session)
        return uow
