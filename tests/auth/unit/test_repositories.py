import pytest
from typing import Optional, List, Sequence
from sqlalchemy import select, CursorResult, Row
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker

from src.auth.models import UserModel
from src.auth.repositories import SQLAlchemyUsersRepository
from src.core.interfaces import BaseModel
from tests.config import TestUserConfig


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_get_success(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_data: Optional[BaseModel] = await SQLAlchemyUsersRepository(session=session).get(id=1)

    assert user_data is not None
    user: UserModel = UserModel(**await user_data.to_dict())
    assert user.id == 1
    assert user.email == TestUserConfig.EMAIL
    assert user.username == TestUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_get_fail(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_data: Optional[BaseModel] = await SQLAlchemyUsersRepository(session=session).get(id=2)
    assert user_data is None


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_get_by_email_success(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_data: Optional[BaseModel] = await SQLAlchemyUsersRepository(session=session).get_by_email(
        email=TestUserConfig.EMAIL
    )

    assert user_data is not None
    user: UserModel = UserModel(**await user_data.to_dict())
    assert user.id == 1
    assert user.email == TestUserConfig.EMAIL
    assert user.username == TestUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_get_by_email_fail(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_data: Optional[BaseModel] = await SQLAlchemyUsersRepository(session=session).get_by_email(
        email='non-existing-email@gmail.com'
    )

    assert user_data is None


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_get_by_username_success(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_data: Optional[BaseModel] = await SQLAlchemyUsersRepository(session=session).get_by_username(
        username=TestUserConfig.USERNAME
    )

    assert user_data is not None
    user: UserModel = UserModel(**await user_data.to_dict())
    assert user.id == 1
    assert user.email == TestUserConfig.EMAIL
    assert user.username == TestUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_get_by_username_fail(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_data: Optional[BaseModel] = await SQLAlchemyUsersRepository(session=session).get_by_username(
        username='non-existing-username'
    )

    assert user_data is None


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_list(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_list: List[BaseModel] = await SQLAlchemyUsersRepository(session=session).list()
    assert len(users_list) == 1
    user: UserModel = UserModel(**await users_list[0].to_dict())
    assert user.id == 1
    assert user.email == TestUserConfig.EMAIL
    assert user.username == TestUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_empty_list(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_list: List[BaseModel] = await SQLAlchemyUsersRepository(session=session).list()
    assert len(users_list) == 0


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_delete_existing_user(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 1

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersRepository(session=session).delete(id=1)

    cursor = await async_connection.execute(select(UserModel))
    result = cursor.all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_delete_non_existing_user(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 0

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersRepository(session=session).delete(id=1)


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_add_user_success(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(email=TestUserConfig.EMAIL))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True))
    await SQLAlchemyUsersRepository(session=session).add(model=user)

    cursor = await async_connection.execute(select(UserModel).filter_by(email=TestUserConfig.EMAIL))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_add_user_success_with_provided_already_existing_id(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    username: str = 'someUsername'
    user: UserModel = UserModel(
        id=1,
        email='someTestEmail@gmail.com',
        username=username,
        password=TestUserConfig.PASSWORD
    )

    await SQLAlchemyUsersRepository(session=session).add(model=user)

    cursor = await async_connection.execute(select(UserModel).filter_by(username=username))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_add_user_fail_username_already_exists(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(username=TestUserConfig.USERNAME))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(
        username=TestUserConfig.USERNAME,
        email='someTestEmail@gmail.com',
        password=TestUserConfig.PASSWORD
    )

    with pytest.raises(IntegrityError):
        await SQLAlchemyUsersRepository(session=session).add(model=user)


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_add_user_fail_email_already_exists(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(email=TestUserConfig.EMAIL))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(
        email=TestUserConfig.EMAIL,
        username='someUsername',
        password=TestUserConfig.PASSWORD
    )

    with pytest.raises(IntegrityError):
        await SQLAlchemyUsersRepository(session=session).add(model=user)


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_update_existing_user(
        map_models_to_orm: None,
        create_test_user_if_not_exists,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    username: str = 'someUsername'
    user: UserModel = UserModel(
        email=TestUserConfig.EMAIL,
        username=username,
        password=TestUserConfig.PASSWORD
    )

    await SQLAlchemyUsersRepository(session=session).update(id=1, model=user)

    cursor = await async_connection.execute(select(UserModel).filter_by(username=username))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_user_repository_update_non_existing_user(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True))
    with pytest.raises(NoResultFound):
        await SQLAlchemyUsersRepository(session=session).update(id=1, model=user)
