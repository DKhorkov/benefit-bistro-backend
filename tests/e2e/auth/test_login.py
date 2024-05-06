import pytest
from fastapi import status
from httpx import Response, AsyncClient

from src.auth.config import RouterConfig, URLPathsConfig, cookies_config
from src.auth.constants import ErrorDetails
from tests.config import TestUserConfig
from tests.utils import get_error_message_from_response


@pytest.mark.anyio
async def test_login_success(async_client: AsyncClient, create_test_user_if_not_exists: None) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json=TestUserConfig().to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get(cookies_config.COOKIES_KEY)


@pytest.mark.anyio
async def test_login_fail_incorrect_email_pattern(
        async_client: AsyncClient,
        create_test_user_if_not_exists: None
) -> None:

    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json={
            'email': 'some_incorrect_email',
            'password': TestUserConfig.PASSWORD
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    expected_error_message: str = ('value is not a valid email address: '
                                   'The email address is not valid. It must have exactly one @-sign.')
    assert get_error_message_from_response(response=response) == expected_error_message


@pytest.mark.anyio
async def test_login_fail_incorrect_email(async_client: AsyncClient, create_test_user_if_not_exists: None) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json={
            'email': 'prefix' + TestUserConfig.EMAIL,
            'password': TestUserConfig.PASSWORD
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_NOT_FOUND


@pytest.mark.anyio
async def test_login_fail_incorrect_password(async_client: AsyncClient, create_test_user_if_not_exists: None) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json={
            'email': TestUserConfig.EMAIL,
            'password': 'prefix' + TestUserConfig.PASSWORD
        }
    )

    assert response.status_code == status.HTTP_412_PRECONDITION_FAILED
    assert get_error_message_from_response(response=response) == ErrorDetails.INVALID_PASSWORD
