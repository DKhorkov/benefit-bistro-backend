from typing import Optional

from src.auth.constants import ErrorDetails
from src.auth.exceptions import UserNotFoundError
from src.auth.models import UserModel
from src.security.models import JWTDataModel
from src.auth.schemas import RegisterUserScheme
from src.auth.interfaces.units_of_work import UsersUnitOfWork
from src.auth.utils import hash_password


class AuthService:
    """
    Service layer according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    async def register_user(self, user_data: RegisterUserScheme) -> UserModel:
        user_data.password = await hash_password(user_data.password)
        async with self._uow as uow:
            user: UserModel = await uow.users.add(UserModel(**user_data.model_dump()))
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
            user: Optional[UserModel]  # declaring here for mypy passing
            if id:
                user = await uow.users.get(id=id)
                if user:
                    return True

            if email:
                user = await uow.users.get_by_email(email)
                if user:
                    return True

            if username:
                user = await uow.users.get_by_username(username)
                if user:
                    return True

            return False

    async def get_user_by_email(self, email: str) -> UserModel:
        async with self._uow as uow:
            user: Optional[UserModel] = await uow.users.get_by_email(email)
            if not user:
                raise UserNotFoundError

            return user

    async def get_user_by_username(self, username: str) -> UserModel:
        async with self._uow as uow:
            user: Optional[UserModel] = await uow.users.get_by_username(username)
            if not user:
                raise UserNotFoundError

            return user

    async def authenticate_user(self, jwt_data: JWTDataModel) -> UserModel:
        async with self._uow as uow:
            user: Optional[UserModel] = await uow.users.get(id=jwt_data.user_id)
            if not user:
                raise UserNotFoundError

            return user

    async def verify_user_email(self, jwt_data: JWTDataModel) -> UserModel:
        async with self._uow as uow:
            user: Optional[UserModel] = await uow.users.get(id=jwt_data.user_id)
            if not user:
                raise UserNotFoundError

            user.email_verified = True
            await uow.users.update(id=jwt_data.user_id, model=user)
            await uow.commit()
            return user
