import pytest
from datetime import datetime, timezone
from typing import List
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.core.database.connection import DATABASE_URL
from src.users.exceptions import (
    UserAlreadyExistsError,
    InvalidPasswordError,
    UserNotFoundError,
    EmailIsNotVerifiedError
)
from src.security.exceptions import InvalidTokenError
from src.users.domain.models import UserModel
from src.security.models import JWTDataModel
from src.users.entrypoints.schemas import RegisterUserScheme, LoginUserScheme
from src.security.utils import create_jwt_token
from tests.config import TestUserConfig
from src.users.entrypoints.dependencies import (
    register_user,
    authenticate_user,
    login_user,
    verify_user_email,
    get_all_users
)


@pytest.mark.anyio
async def test_register_user_success(map_models_to_orm: None) -> None:
    user_data: RegisterUserScheme = RegisterUserScheme(**TestUserConfig().to_dict(to_lower=True))
    user: UserModel = await register_user(user_data=user_data)

    assert user.id == 1
    assert user.username == TestUserConfig.USERNAME
    assert user.email == TestUserConfig.EMAIL
    assert not user.password


@pytest.mark.anyio
async def test_register_user_fail(create_test_user_if_not_exists: None) -> None:
    user_data: RegisterUserScheme = RegisterUserScheme(**TestUserConfig().to_dict(to_lower=True))
    with pytest.raises(UserAlreadyExistsError):
        await register_user(user_data=user_data)


@pytest.mark.anyio
async def test_login_user_by_username_success(create_test_user_if_not_exists: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(username=TestUserConfig.USERNAME, password=TestUserConfig.PASSWORD)
    user: UserModel = await login_user(user_data=user_data)

    assert user.id == 1
    assert user.username == TestUserConfig.USERNAME
    assert user.email == TestUserConfig.EMAIL
    assert not user.password


@pytest.mark.anyio
async def test_login_user_by_email_success(create_test_user_if_not_exists: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(username=TestUserConfig.EMAIL, password=TestUserConfig.PASSWORD)
    user: UserModel = await login_user(user_data=user_data)

    assert user.id == 1
    assert user.username == TestUserConfig.USERNAME
    assert user.email == TestUserConfig.EMAIL
    assert not user.password


@pytest.mark.anyio
async def test_login_user_fail_user_does_not_exist(map_models_to_orm: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(**TestUserConfig().to_dict(to_lower=True))
    with pytest.raises(UserNotFoundError):
        await login_user(user_data=user_data)


@pytest.mark.anyio
async def test_login_user_fail_incorrect_password(create_test_user_if_not_exists: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(**TestUserConfig().to_dict(to_lower=True))
    user_data.password = 'some_incorrect_password'
    with pytest.raises(InvalidPasswordError):
        await login_user(user_data=user_data)


@pytest.mark.anyio
async def test_login_user_fail_email_is_not_verified(create_test_user_if_not_exists: None) -> None:
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        try:
            await conn.execute(update(UserModel).values(email_verified=False).filter_by(email=TestUserConfig.EMAIL))
            await conn.commit()
        except IntegrityError:
            await conn.rollback()

    with pytest.raises(EmailIsNotVerifiedError):
        await login_user(user_data=LoginUserScheme(**TestUserConfig().to_dict(to_lower=True)))


@pytest.mark.anyio
async def test_authenticate_user_success(map_models_to_orm: None, access_token: str) -> None:
    user: UserModel = await authenticate_user(token=access_token)
    assert user.email == TestUserConfig.EMAIL
    assert user.username == TestUserConfig.USERNAME
    assert not user.password


@pytest.mark.anyio
async def test_authenticate_user_fail_invalid_token(map_models_to_orm: None) -> None:
    with pytest.raises(InvalidTokenError):
        await authenticate_user(token='someInvalidToken')


@pytest.mark.anyio
async def test_authenticate_user_fail_token_expired(map_models_to_orm: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1, exp=datetime.now(timezone.utc))
    token: str = await create_jwt_token(jwt_data=jwt_data)
    with pytest.raises(InvalidTokenError):
        await authenticate_user(token=token)


@pytest.mark.anyio
async def test_authenticate_user_fail_user_does_not_exist(map_models_to_orm: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    with pytest.raises(UserNotFoundError):
        await authenticate_user(token=token)


@pytest.mark.anyio
async def test_verify_user_email_success(access_token: str) -> None:
    user: UserModel = await verify_user_email(token=access_token)
    assert user.email_verified
    assert not user.password


@pytest.mark.anyio
async def test_verify_user_email_fail_user_does_not_exist(map_models_to_orm: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    with pytest.raises(UserNotFoundError):
        await verify_user_email(token=token)


@pytest.mark.anyio
async def test_get_all_users_with_existing_user(create_test_user_if_not_exists: None) -> None:
    users: List[UserModel] = await get_all_users()
    assert len(users) == 1
    user: UserModel = users[0]
    assert user.id == 1
    assert user.username == TestUserConfig.USERNAME
    assert user.email == TestUserConfig.EMAIL
    assert not user.password


@pytest.mark.anyio
async def test_get_all_users_with_no_existing_users(map_models_to_orm: None) -> None:
    users: List[UserModel] = await get_all_users()
    assert len(users) == 0
