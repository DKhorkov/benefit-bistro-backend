from typing import Optional

from src.auth.constants import ErrorDetails
from src.auth.exceptions import UserNotFoundError
from src.auth.models import UserModel
from src.security.models import JWTDataModel
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

    async def register_user(self, user_data: RegisterUserScheme) -> UserModel:
        user_data.password = await hash_password(user_data.password)
        user: UserModel = UserModel(**user_data.model_dump())
        async with self._uow as uow:
            result: BaseModel = await uow.users.add(user)
            user = UserModel(**await result.to_dict())
            await uow.commit()
            return user

    async def check_user_existence(
            self,
            id: Optional[int] = None,
            email: Optional[str] = None,
            username: Optional[str] = None
    ) -> bool:

        if not (id or email or username):
            raise ValueError(ErrorDetails.USER_ATTRIBUTE_REQUIRED)

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

    async def verify_user_email(self, jwt_data: JWTDataModel) -> UserModel:
        async with self._uow as uow:
            result: Optional[BaseModel] = await uow.users.get(id=jwt_data.user_id)
            if not result:
                raise UserNotFoundError

            user = UserModel(**await result.to_dict())
            user.email_verified = True
            await uow.users.update(id=jwt_data.user_id, model=user)
            await uow.commit()
            return user
