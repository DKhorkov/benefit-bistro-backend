import pytest
from typing import List

from src.users.constants import ErrorDetails
from src.users.exceptions import UserNotFoundError
from src.users.interfaces.repositories import UsersRepository
from src.users.interfaces.units_of_work import UsersUnitOfWork
from src.users.models import UserModel
from src.security.models import JWTDataModel
from src.users.schemas import RegisterUserScheme
from src.users.service import UsersService
from tests.users.fake_objects import FakeUsersUnitOfWork, FakeUsersRepository
from tests.config import TestUserConfig


def create_fake_users_repository_instance(with_user: bool = False) -> UsersRepository:
    users_repository: UsersRepository
    if with_user:
        user_id: int = 1
        user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True), id=user_id)
        users_repository = FakeUsersRepository(users={user_id: user})
    else:
        users_repository = FakeUsersRepository()

    return users_repository


@pytest.mark.anyio
async def test_users_service_register_user_success() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    user_data: RegisterUserScheme = RegisterUserScheme(**TestUserConfig().to_dict(to_lower=True))
    await users_service.register_user(user_data=user_data)
    assert len(await users_repository.list()) == 1


@pytest.mark.anyio
async def test_users_service_authenticate_user_success() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    found_user: UserModel = await users_service.authenticate_user(jwt_data=jwt_data)
    assert found_user.email == TestUserConfig.EMAIL
    assert found_user.username == TestUserConfig.USERNAME
    assert found_user.id == 1


@pytest.mark.anyio
async def test_users_service_authenticate_user_fail() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    with pytest.raises(UserNotFoundError):
        await users_service.authenticate_user(jwt_data=jwt_data)


@pytest.mark.anyio
async def test_users_service_get_user_by_email_success() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    found_user: UserModel = await users_service.get_user_by_email(email=TestUserConfig.EMAIL)
    assert found_user.email == TestUserConfig.EMAIL
    assert found_user.username == TestUserConfig.USERNAME
    assert found_user.id == 1


@pytest.mark.anyio
async def test_users_service_get_user_by_email_fail() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    with pytest.raises(UserNotFoundError):
        await users_service.get_user_by_email(email=TestUserConfig.EMAIL)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_id() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    assert await users_service.check_user_existence(id=1)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_email() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    assert await users_service.check_user_existence(email=TestUserConfig.EMAIL)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_username() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    assert await users_service.check_user_existence(username=TestUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_check_user_existence_fail_user_does_not_exist() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    assert not await users_service.check_user_existence(username=TestUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_check_user_existence_fail_no_attributes_provided() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)
    with pytest.raises(ValueError) as exc_info:
        await users_service.check_user_existence()

    assert str(exc_info.value) == ErrorDetails.USER_ATTRIBUTE_REQUIRED


@pytest.mark.anyio
async def test_verify_user_email_success() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    user: UserModel = await users_service.verify_user_email(jwt_data=jwt_data)

    assert user.email_verified


@pytest.mark.anyio
async def test_verify_user_email_fail() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    with pytest.raises(UserNotFoundError):
        await users_service.verify_user_email(jwt_data=jwt_data)


@pytest.mark.anyio
async def test_users_service_get_user_by_username_success() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    found_user: UserModel = await users_service.get_user_by_username(username=TestUserConfig.USERNAME)
    assert found_user.email == TestUserConfig.EMAIL
    assert found_user.username == TestUserConfig.USERNAME
    assert found_user.id == 1


@pytest.mark.anyio
async def test_users_service_get_user_by_username_fail() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    with pytest.raises(UserNotFoundError):
        await users_service.get_user_by_username(username=TestUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_get_all_users_with_existing_user() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    users: List[UserModel] = await users_service.get_all_users()
    assert len(users) == 1


@pytest.mark.anyio
async def test_users_service_get_all_users_with_no_existing_users() -> None:
    users_repository: UsersRepository = create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    users: List[UserModel] = await users_service.get_all_users()
    assert len(users) == 0
