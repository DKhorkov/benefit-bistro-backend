import pytest
from fastapi import status
from httpx import Response

from src.auth.config import RouterConfig, URLPathsConfig, cookies_config


@pytest.mark.anyio
async def test_logout(async_client, cookies) -> None:
    response: Response = await async_client.get(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGOUT,
        cookies=cookies
    )

    assert response.status_code == status.HTTP_200_OK
    assert not response.cookies.get(cookies_config.COOKIES_KEY)
