import pytest
from fastapi import status
from httpx import Response

from src.config import URLPathsConfig


@pytest.mark.anyio
async def test_homepage(async_client) -> None:
    response: Response = await async_client.get(url=URLPathsConfig.HOMEPAGE)
    assert response.status_code == status.HTTP_200_OK
