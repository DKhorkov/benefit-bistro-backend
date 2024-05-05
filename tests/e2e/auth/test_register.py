import pytest
from fastapi import status
from httpx import Response

from src.auth.config import RouterConfig, URLPathsConfig, UserValidationConfig
from src.auth.constants import ErrorDetails
from tests.utils import get_error_message_from_response, generate_random_string


@pytest.mark.anyio
async def test_register_fail_incorrect_email_pattern(async_client, create_test_user_if_not_exists) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json={
            'email': 'some_incorrect_email',
            'password': 'some_password',
            'username': 'some_username'
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    expected_error_message: str = ('value is not a valid email address: '
                                   'The email address is not valid. It must have exactly one @-sign.')
    assert get_error_message_from_response(response=response) == expected_error_message


@pytest.mark.anyio
async def test_register_fail_too_short_username(async_client, create_test_user_if_not_exists) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json={
            'email': 'some_email@mail.ru',
            'password': 'some_password',
            'username': generate_random_string(length=UserValidationConfig.USERNAME_MIN_LENGTH - 1)
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.USERNAME_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_fail_too_long_username(async_client, create_test_user_if_not_exists) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json={
            'email': 'some_email@mail.ru',
            'password': 'some_password',
            'username': generate_random_string(length=UserValidationConfig.USERNAME_MAX_LENGTH + 1)
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.USERNAME_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_fail_too_short_password(async_client, create_test_user_if_not_exists) -> None:
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
async def test_register_fail_too_long_password(async_client, create_test_user_if_not_exists) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json={
            'email': 'some_email@mail.ru',
            'password': generate_random_string(length=UserValidationConfig.PASSWORD_MAX_LENGTH + 1),
            'username': 'some_username'
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.PASSWORD_VALIDATION_ERROR


@pytest.mark.anyio
async def test_register_success(async_client, create_test_user_if_not_exists) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json={
            'email': 'some_email@mail.ru',
            'password': 'some_password',
            'username': 'some_username'
        }
    )

    assert response.status_code == status.HTTP_303_SEE_OTHER


@pytest.mark.anyio
async def test_register_fail_email_already_taken(async_client, create_test_user_if_not_exists) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json={
            'email': 'some_email@mail.ru',
            'password': 'some_password',
            'username': 'some_new_username'
        }
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_ALREADY_EXISTS


@pytest.mark.anyio
async def test_register_fail_username_already_taken(async_client, create_test_user_if_not_exists) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.REGISTER,
        json={
            'email': 'some_new_email@mail.ru',
            'password': 'some_password',
            'username': 'some_username'
        }
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_ALREADY_EXISTS
