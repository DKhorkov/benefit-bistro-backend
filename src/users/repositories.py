from typing import List, Optional
from sqlalchemy import insert, select, delete, update, Result

from src.users.interfaces.repositories import UsersRepository
from src.users.models import UserModel
from src.core.database.interfaces.repositories import SQLAlchemyAbstractRepository
from src.core.interfaces import AbstractModel


class SQLAlchemyUsersRepository(SQLAlchemyAbstractRepository, UsersRepository):

    async def get(self, id: int) -> Optional[UserModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(email=email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(username=username))
        return result.scalar_one_or_none()

    async def add(self, model: AbstractModel) -> UserModel:
        result: Result = await self._session.execute(
            insert(UserModel).values(**await model.to_dict(exclude={'id'})).returning(UserModel)
        )

        return result.scalar_one()

    async def update(self, id: int, model: AbstractModel) -> UserModel:
        result: Result = await self._session.execute(
            update(UserModel).filter_by(id=id).values(**await model.to_dict(exclude={'id'})).returning(UserModel)
        )

        return result.scalar_one()

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(UserModel).filter_by(id=id))

    async def list(self) -> List[UserModel]:
        result: Result = await self._session.execute(select(UserModel))

        # Using this type casting for purpose of passing mypy checks:
        return [UserModel(**await r.to_dict()) for r in result.scalars().all()]
