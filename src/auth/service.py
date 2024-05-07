from typing import Optional

from src.auth.exceptions import UserNotFoundError
from src.auth.models import UserModel
from src.auth.models import JWTDataModel
from src.auth.schemas import RegisterUserScheme
from src.auth.interfaces.units_of_work import UsersUnitOfWork
from src.auth.utils import hash_password
from src.core.interfaces import BaseModel


class AuthService:
    """
    Service layer according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    async def register_user(self, user_data: RegisterUserScheme) -> None:
        user_data.password = await hash_password(user_data.password)
        user: UserModel = UserModel(**user_data.model_dump())
        async with self._uow as uow:
            await uow.users.add(user)
            await uow.commit()

    async def check_user_existence(
            self,
            id: Optional[int] = None,
            email: Optional[str] = None,
            username: Optional[str] = None
    ) -> bool:

        if not (id or email or username):
            raise ValueError('user id, email or username is required')

        async with self._uow as uow:
            result: Optional[BaseModel]  # declaring here for mypy passing
            if id:
                result = await uow.users.get(id=id)
                if result:
                    return True

            if email:
                result = await uow.users.get_by_email(email)
                if result:
                    return True

            if username:
                result = await uow.users.get_by_username(username)
                if result:
                    return True

            return False

    async def get_user_by_email(self, email: str) -> UserModel:
        async with self._uow as uow:
            result: Optional[BaseModel] = await uow.users.get_by_email(email)

            if not result:
                raise UserNotFoundError

            return UserModel(**await result.to_dict())

    async def authenticate_user(self, jwt_data: JWTDataModel) -> UserModel:
        async with self._uow as uow:
            result: Optional[BaseModel] = await uow.users.get(id=jwt_data.user_id)

            if not result:
                raise UserNotFoundError

            return UserModel(**await result.to_dict())
