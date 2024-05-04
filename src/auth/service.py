from typing import Optional

from src.auth.exceptions import UserNotFound
from src.auth.models import UserModel
from src.auth.models import JWTDataModel
from src.auth.schemas import RegisterUserScheme
from src.auth.units_of_work import UsersUnitOfWork
from src.auth.utils import hash_password
from src.core.interfaces import BaseModel


class AuthService:

    uow: UsersUnitOfWork = UsersUnitOfWork()

    @classmethod
    async def register_user(cls, user_data: RegisterUserScheme) -> None:
        user_data.password = await hash_password(user_data.password)
        user: UserModel = UserModel(**user_data.model_dump())
        async with cls.uow as uow:
            await uow.users.add(user)
            await uow.commit()

    @classmethod
    async def check_user_existence(cls, id: Optional[int] = None, email: Optional[str] = None) -> bool:
        if not (id or email):
            raise ValueError('user id or email is required')

        async with cls.uow as uow:
            result: Optional[BaseModel]  # declaring here for mypy passing
            if id:
                result = await uow.users.get(id=id)
            elif email:
                result = await uow.users.get_by_email(email)

            if result:
                return True

            return False

    @classmethod
    async def get_user_by_email(cls, email: str) -> UserModel:
        async with cls.uow as uow:
            result: Optional[BaseModel] = await uow.users.get_by_email(email)

            if not result:
                raise UserNotFound

            return UserModel(** await result.to_dict())

    @classmethod
    async def authenticate_user(cls, jwt_data: JWTDataModel) -> UserModel:
        async with cls.uow as uow:
            result: Optional[BaseModel] = await uow.users.get(id=jwt_data.user_id)

            if not result:
                raise UserNotFound

            return UserModel(** await result.to_dict())
