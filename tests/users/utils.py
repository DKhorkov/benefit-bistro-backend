from src.users.domain.models import UserModel
from src.users.interfaces import UsersRepository
from src.users.utils import hash_password
from tests.config import FakeUserConfig
from tests.users.fake_objects import FakeUsersRepository


async def create_fake_users_repository_instance(with_user: bool = False) -> UsersRepository:
    users_repository: UsersRepository
    if with_user:
        user_id: int = 1
        user_data: FakeUserConfig = FakeUserConfig()
        user_data.PASSWORD = await hash_password(user_data.PASSWORD)
        user: UserModel = UserModel(**user_data.to_dict(to_lower=True), id=user_id)
        users_repository = FakeUsersRepository(users={user_id: user})
    else:
        users_repository = FakeUsersRepository()

    return users_repository
