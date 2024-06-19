from typing import Self

from src.groups.interfaces.repositories import GroupsRepository
from src.groups.interfaces.units_of_work import GroupsUnitOfWork
from src.groups.adapters.repositories import SQLAlchemyGroupsRepository
from src.core.database.interfaces.units_of_work import SQLAlchemyAbstractUnitOfWork


class SQLAlchemyGroupsUnitOfWork(SQLAlchemyAbstractUnitOfWork, GroupsUnitOfWork):

    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.groups: GroupsRepository = SQLAlchemyGroupsRepository(session=self._session)
        return uow
