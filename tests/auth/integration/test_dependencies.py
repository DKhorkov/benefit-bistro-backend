import pytest
from datetime import datetime, timezone

from src.auth.dependencies import register_user, authenticate_user, login_user
from src.auth.exceptions import UserAlreadyExistError, InvalidPasswordError, UserNotFoundError, InvalidTokenError
from src.auth.models import UserModel, JWTDataModel
from src.auth.schemas import RegisterUserScheme, LoginUserScheme
from src.auth.utils import create_access_token
from tests.config import TestUserConfig


@pytest.mark.anyio
async def test_register_user_success(map_models_to_orm: None) -> None:
    user_data: RegisterUserScheme = RegisterUserScheme(**TestUserConfig().to_dict(to_lower=True))
    await register_user(user_data=user_data)


@pytest.mark.anyio
async def test_register_user_fail(map_models_to_orm: None, create_test_user_if_not_exists: None) -> None:
    user_data: RegisterUserScheme = RegisterUserScheme(**TestUserConfig().to_dict(to_lower=True))
    with pytest.raises(UserAlreadyExistError):
        await register_user(user_data=user_data)


@pytest.mark.anyio
async def test_login_user_success(map_models_to_orm: None, create_test_user_if_not_exists: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(**TestUserConfig().to_dict(to_lower=True))
    await login_user(user_data=user_data)


@pytest.mark.anyio
async def test_login_user_fail_user_does_not_exist(map_models_to_orm: None) -> None:
    user_data: LoginUserScheme = LoginUserScheme(**TestUserConfig().to_dict(to_lower=True))
    with pytest.raises(UserNotFoundError):
        await login_user(user_data=user_data)


@pytest.mark.anyio
async def test_login_user_fail_incorrect_password(
        map_models_to_orm: None,
        create_test_user_if_not_exists: None
) -> None:

    user_data: LoginUserScheme = LoginUserScheme(**TestUserConfig().to_dict(to_lower=True))
    user_data.password = 'some_incorrect_password'
    with pytest.raises(InvalidPasswordError):
        await login_user(user_data=user_data)


@pytest.mark.anyio
async def test_authenticate_user_success(map_models_to_orm: None, access_token: str) -> None:
    user: UserModel = await authenticate_user(token=access_token)
    assert user.email == TestUserConfig.EMAIL
    assert user.username == TestUserConfig.USERNAME


@pytest.mark.anyio
async def test_authenticate_user_fail_invalid_token(map_models_to_orm: None) -> None:
    with pytest.raises(InvalidTokenError):
        await authenticate_user(token='someInvalidToken')


@pytest.mark.anyio
async def test_authenticate_user_fail_token_expired(map_models_to_orm: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1, exp=datetime.now(timezone.utc))
    token: str = await create_access_token(jwt_data=jwt_data)
    with pytest.raises(InvalidTokenError):
        await authenticate_user(token=token)


@pytest.mark.anyio
async def test_authenticate_user_fail_user_does_not_exist(map_models_to_orm: None) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=1)
    token: str = await create_access_token(jwt_data=jwt_data)
    with pytest.raises(UserNotFoundError):
        await authenticate_user(token=token)
