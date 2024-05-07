from typing import List, Optional
from sqlalchemy import insert, select, delete, update, Result

from src.auth.interfaces.repositories import UsersRepository
from src.auth.models import UserModel
from src.core.database.repositories import SQLAlchemyRepository
from src.core.interfaces import BaseModel


class SQLAlchemyUsersRepository(SQLAlchemyRepository, UsersRepository):

    async def get(self, id: int) -> Optional[BaseModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(id=id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[BaseModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(email=email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[BaseModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(username=username))
        return result.scalar_one_or_none()

    async def add(self, model: BaseModel) -> None:
        await self._session.execute(insert(UserModel).values(**await model.to_dict(exclude={'id'})))

    async def update(self, id: int, model: BaseModel) -> None:
        await self._session.execute(update(UserModel).filter_by(id=id).values(**await model.to_dict(exclude={'id'})))

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(UserModel).filter_by(id=id))

    async def list(self) -> List[BaseModel]:
        result: Result = await self._session.execute(select(UserModel))

        # Using this type casting for purpose of passing mypy checks:
        return [UserModel(**await r.to_dict()) for r in result.scalars().all()]
