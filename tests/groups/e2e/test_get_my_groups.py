import pytest
from fastapi import status
from typing import List, Dict, Any
from httpx import Response, AsyncClient, Cookies

from src.groups.config import RouterConfig, URLPathsConfig
from src.groups.domain.models import GroupModel
from tests.config import FakeGroupConfig


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
    groups: List[GroupModel] = list()

    group_data: Dict[str, Any]
    for group_data in response.json():
        group_data.pop('members')
        groups.append(GroupModel(**group_data))

    assert len(groups) == 1
    group: GroupModel = groups[0]
    assert group.name == FakeGroupConfig.NAME
    assert len(group.members) == 0


@pytest.mark.anyio
async def test_get_my_groups_fail(
        async_client: AsyncClient,
        create_test_group: None
) -> None:

    response: Response = await async_client.get(url=RouterConfig.PREFIX + URLPathsConfig.MY_GROUPS)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
