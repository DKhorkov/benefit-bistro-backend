import pytest
from fastapi import status
from httpx import Response, AsyncClient

from src.users.config import RouterConfig, URLPathsConfig
from src.security.constants import ErrorDetails as SecurityErrorDetails
from src.users.constants import ErrorDetails as AuthErrorDetails
from src.core.utils import get_symbols_before_selected_chars
from src.security.models import JWTDataModel
from src.security.utils import create_jwt_token
from tests.utils import get_error_message_from_response


@pytest.mark.anyio
async def test_verify_email_success(async_client: AsyncClient, access_token: str) -> None:
    verify_email_url_base: str = get_symbols_before_selected_chars(
        chars='{',
        string=URLPathsConfig.VERIFY_EMAIL
    )

    response: Response = await async_client.get(
        url=RouterConfig.PREFIX + verify_email_url_base + access_token
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_verify_email_fail_user_does_not_exist(async_client: AsyncClient) -> None:
    jwt_data: JWTDataModel = JWTDataModel(user_id=2)
    token: str = await create_jwt_token(jwt_data=jwt_data)
    verify_email_url_base: str = get_symbols_before_selected_chars(
        chars='{',
        string=URLPathsConfig.VERIFY_EMAIL
    )

    response: Response = await async_client.get(
        url=RouterConfig.PREFIX + verify_email_url_base + token
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert get_error_message_from_response(response=response) == AuthErrorDetails.USER_NOT_FOUND


@pytest.mark.anyio
async def test_verify_email_fail_invalid_token(async_client: AsyncClient, create_test_user_if_not_exists: None) -> None:
    verify_email_url_base: str = get_symbols_before_selected_chars(
        chars='{',
        string=URLPathsConfig.VERIFY_EMAIL
    )

    response: Response = await async_client.get(
        url=RouterConfig.PREFIX + verify_email_url_base + 'someInvalidToken'
    )

    assert response.status_code == status.HTTP_412_PRECONDITION_FAILED
    assert get_error_message_from_response(response=response) == SecurityErrorDetails.INVALID_TOKEN
