from typing import List, Optional
from sqlalchemy import insert, select, delete, update, Result

from src.auth.models import UserModel
from src.core.database.repositories import SQLAlchemyRepository
from src.core.interfaces import BaseModel


class UsersRepository(SQLAlchemyRepository):

    async def get(self, id: int) -> Optional[BaseModel]:
        result: Result = await self._session.execute(select(UserModel).filter_by(id=id))
        user: Optional[UserModel] = result.scalar_one_or_none()
        return user

    async def get_by_email(self, email: str) -> Optional[BaseModel]:
        result: Result = await self._session.execute(select(UserModel).options().filter_by(email=email))
        user: Optional[UserModel] = result.scalar_one_or_none()
        return user

    async def add(self, model: BaseModel) -> None:
        await self._session.execute(insert(UserModel).values(** await model.to_dict(exclude={'id'})))

    async def update(self, id: int, model: BaseModel) -> None:
        await self._session.execute(update(UserModel).filter_by(id=id).values(** await model.to_dict(exclude={'id'})))

    async def delete(self, id: int) -> None:
        await self._session.execute(delete(UserModel).filter_by(id=id))

    async def list(self) -> List[BaseModel]:
        result: Result = await self._session.execute(select(UserModel))
        users = result.scalars().all()
        return [UserModel(**r._asdict()) for r in users]
