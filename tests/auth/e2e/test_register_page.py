import pytest
from fastapi import status
from httpx import Response, AsyncClient

from src.auth.config import URLPathsConfig, RouterConfig


@pytest.mark.anyio
async def test_register_page(async_client: AsyncClient) -> None:
    response: Response = await async_client.get(url=RouterConfig.PREFIX + URLPathsConfig.REGISTER_PAGE)
    assert response.status_code == status.HTTP_200_OK
