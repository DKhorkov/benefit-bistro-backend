import pytest
from fastapi import status
from httpx import Response, AsyncClient
from typing import Dict, Any

from src.auth.config import RouterConfig, URLPathsConfig, UserValidationConfig
from src.auth.constants import ErrorDetails
from tests.utils import get_error_message_from_response, generate_random_string
from tests.config import TestUserConfig


@pytest.mark.anyio
async def test_register_fail_incorrect_email_pattern(async_client: AsyncClient) -> None:
    test_user_config: Dict[str, Any] = TestUserConfig().to_dict(to_lower=True)
    test_user_config['email'] = '<EMAIL>'
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    expected_error_message: str = ('value is not a valid email address: '
                                   'The email address is not valid. It must have exactly one @-sign.')
    assert get_error_message_from_response(response=response) == expected_error_message


@pytest.mark.anyio
async def test_register_fail_too_short_username(async_client: AsyncClient) -> None:
    test_user_config: Dict[str, Any] = TestUserConfig().to_dict(to_lower=True)
    test_user_config['username'] = generate_random_string(length=UserValidationConfig.USERNAME_MIN_LENGTH - 1)
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.USERNAME_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_fail_too_long_username(async_client: AsyncClient) -> None:
    test_user_config: Dict[str, Any] = TestUserConfig().to_dict(to_lower=True)
    test_user_config['username'] = generate_random_string(length=UserValidationConfig.USERNAME_MAX_LENGTH + 1)
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.USERNAME_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_fail_too_short_password(async_client: AsyncClient) -> None:
    test_user_config: Dict[str, Any] = TestUserConfig().to_dict(to_lower=True)
    test_user_config['password'] = generate_random_string(length=UserValidationConfig.PASSWORD_MIN_LENGTH - 1),
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json={
            'email': 'some_email@mail.ru',
            'password': generate_random_string(length=UserValidationConfig.PASSWORD_MIN_LENGTH - 1),
            'username': 'some_username'
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.PASSWORD_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_fail_too_long_password(async_client: AsyncClient) -> None:
    test_user_config: Dict[str, Any] = TestUserConfig().to_dict(to_lower=True)
    test_user_config['password'] = generate_random_string(length=UserValidationConfig.PASSWORD_MIN_LENGTH + 1),
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.PASSWORD_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_success(async_client: AsyncClient) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=TestUserConfig().to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.has_redirect_location


@pytest.mark.anyio
async def test_register_fail_email_already_taken(
        async_client: AsyncClient,
        create_test_user_if_not_exists: None
) -> None:

    test_user_config: Dict[str, Any] = TestUserConfig().to_dict(to_lower=True)
    test_user_config['username'] = 'some_new_username'
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_ALREADY_EXISTS


@pytest.mark.anyio
async def test_register_fail_username_already_taken(
        async_client: AsyncClient,
        create_test_user_if_not_exists: None
) -> None:

    test_user_config: Dict[str, Any] = TestUserConfig().to_dict(to_lower=True)
    test_user_config['email'] = 'some_new_email@mail.ru'
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json=test_user_config
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_ALREADY_EXISTS
