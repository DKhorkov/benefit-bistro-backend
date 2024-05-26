import pytest
from fastapi import status
from httpx import Response, AsyncClient

from src.users.config import RouterConfig, URLPathsConfig, cookies_config
from src.users.constants import ErrorDetails
from tests.config import TestUserConfig
from tests.utils import get_error_message_from_response


@pytest.mark.anyio
async def test_login_by_email_success(async_client: AsyncClient, create_test_user_if_not_exists: None) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json={
            'username': TestUserConfig.EMAIL,
            'password': TestUserConfig.PASSWORD
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get(cookies_config.COOKIES_KEY)


@pytest.mark.anyio
async def test_login_by_username_success(async_client: AsyncClient, create_test_user_if_not_exists: None) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json={
            'username': TestUserConfig.USERNAME,
            'password': TestUserConfig.PASSWORD
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get(cookies_config.COOKIES_KEY)


@pytest.mark.anyio
async def test_login_fail_user_not_found(async_client: AsyncClient, map_models_to_orm: None) -> None:
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json=TestUserConfig().to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert get_error_message_from_response(response=response) == ErrorDetails.USER_NOT_FOUND


@pytest.mark.anyio
async def test_login_fail_incorrect_password(async_client: AsyncClient, create_test_user_if_not_exists: None) -> None:
    test_user_config: TestUserConfig = TestUserConfig()
    test_user_config.PASSWORD = 'incorrectPassword'
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json=test_user_config.to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_412_PRECONDITION_FAILED
    assert get_error_message_from_response(response=response) == ErrorDetails.INVALID_PASSWORD
