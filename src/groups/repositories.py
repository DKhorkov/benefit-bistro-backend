from typing import List, Optional
from sqlalchemy import insert, select, delete, update, Result

from src.groups.interfaces.repositories import GroupsRepository
from src.groups.models import GroupModel
from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.core.interfaces import AbstractModel


class SQLAlchemyGroupsRepository(SQLAlchemyAbstractRepository, GroupsRepository):

    async def get(self, id: int) -> Optional[GroupModel]:
        result: Result = await self._session.execute(select(GroupModel).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_owner_and_name(self, name: str, owner_id: int) -> Optional[GroupModel]:
        result: Result = await self._session.execute(select(GroupModel).filter_by(name=name, owner_id=owner_id))
        return result.scalar_one_or_none()

    async def get_owner_groups(self, owner_id: int) -> List[GroupModel]:
        result: Result = await self._session.execute(select(GroupModel).filter_by(owner_id=owner_id))

        # Using this type casting for purpose of passing mypy checks:
        return [GroupModel(**await r.to_dict()) for r in result.scalars().all()]

    async def add(self, model: AbstractModel) -> GroupModel:
        result: Result = await self._session.execute(
            insert(GroupModel).values(**await model.to_dict(exclude={'id', 'members'})).returning(GroupModel)
        )

        return result.scalar_one()

    async def update(self, id: int, model: AbstractModel) -> GroupModel:
        result: Result = await self._session.execute(
            update(
                GroupModel
            ).filter_by(
                id=id
            ).values(
                **await model.to_dict(exclude={'id', 'members'})
            ).returning(
                GroupModel
            )
        )

        return result.scalar_one()

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(GroupModel).filter_by(id=id))

    async def list(self) -> List[GroupModel]:
        result: Result = await self._session.execute(select(GroupModel))

        # Using this type casting for purpose of passing mypy checks:
        return [GroupModel(**await r.to_dict()) for r in result.scalars().all()]
