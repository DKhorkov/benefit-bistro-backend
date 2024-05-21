import pytest
from fastapi import status
from typing import List
from httpx import Response, AsyncClient, Cookies

from src.groups.config import RouterConfig, URLPathsConfig
from src.groups.models import GroupModel
from tests.config import TestGroupConfig


@pytest.mark.anyio
async def test_get_my_groups_success(
        async_client: AsyncClient,
        create_test_group: None,
        cookies: Cookies
) -> None:

    response: Response = await async_client.get(
        url=RouterConfig.PREFIX + URLPathsConfig.MY_GROUPS,
        cookies=cookies
    )

    assert response.status_code == status.HTTP_200_OK
    groups: List[GroupModel] = [GroupModel(**group) for group in response.json()]
    assert len(groups) == 1
    assert groups[0].name == TestGroupConfig.NAME


@pytest.mark.anyio
async def test_get_my_groups_fail(
        async_client: AsyncClient,
        create_test_group: None
) -> None:

    response: Response = await async_client.get(url=RouterConfig.PREFIX + URLPathsConfig.MY_GROUPS)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
