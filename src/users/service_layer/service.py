from typing import Optional, List

from src.users.constants import ErrorDetails
from src.users.exceptions import UserNotFoundError
from src.users.domain.models import UserModel
from src.users.interfaces.units_of_work import UsersUnitOfWork


class UsersService:
    """
    Service layer core according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow: UsersUnitOfWork = uow

    async def register_user(self, user: UserModel) -> UserModel:
        async with self._uow as uow:
            user = await uow.users.add(model=user)
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

    async def get_user_by_id(self, id: int) -> UserModel:
        async with self._uow as uow:
            user: Optional[UserModel] = await uow.users.get(id=id)
            if not user:
                raise UserNotFoundError

            return user

    async def verify_user_email(self, id: int) -> UserModel:
        async with self._uow as uow:
            user: Optional[UserModel] = await uow.users.get(id=id)
            if not user:
                raise UserNotFoundError

            user.email_verified = True
            await uow.commit()
            return user

    async def get_all_users(self) -> List[UserModel]:
        async with self._uow as uow:
            users: List[UserModel] = await uow.users.list()
            return users
