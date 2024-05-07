from typing import Dict, Optional, List

from src.auth.interfaces.units_of_work import UsersUnitOfWork
from src.auth.interfaces.repositories import UsersRepository
from src.auth.models import UserModel
from src.core.interfaces import BaseModel


class FakeUsersRepository(UsersRepository):

    def __init__(self, users: Optional[Dict[int, BaseModel]] = None) -> None:
        self.users: Dict[int, BaseModel] = users if users else {}

    async def get(self, id: int) -> Optional[BaseModel]:
        return self.users.get(id)

    async def get_by_email(self, email: str) -> Optional[BaseModel]:
        for user in self.users.values():
            current_user: UserModel = UserModel(**await user.to_dict())
            if current_user.email == email:
                return user

        return None

    async def get_by_username(self, username: str) -> Optional[BaseModel]:
        for user in self.users.values():
            current_user: UserModel = UserModel(**await user.to_dict())
            if current_user.username == username:
                return user

        return None

    async def add(self, model: BaseModel) -> None:
        user: UserModel = UserModel(**await model.to_dict())
        self.users[user.id] = model

    async def update(self, id: int, model: BaseModel) -> None:
        if id in self.users:
            self.users[id] = model

    async def delete(self, id: int) -> None:
        if id in self.users:
            del self.users[id]

    async def list(self) -> List[BaseModel]:
        return list(self.users.values())


class FakeUsersUnitOfWork(UsersUnitOfWork):

    def __init__(self, users_repository: UsersRepository) -> None:
        self.users: UsersRepository = users_repository
        self.committed: bool = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass
