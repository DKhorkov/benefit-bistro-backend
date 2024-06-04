import pytest
from fastapi import status
from httpx import Response, AsyncClient, Cookies
from typing import Dict, Any

from src.core.utils import get_substring_before_chars, get_substring_after_chars
from src.groups.config import RouterConfig, URLPathsConfig
from src.groups.constants import ErrorDetails
from tests.utils import get_error_message_from_response
from tests.config import TestGroupMembersConfig


@pytest.mark.anyio
async def test_update_group_members_success(
        async_client: AsyncClient,
        create_test_group: None,
        cookies: Cookies
) -> None:

    update_group_members_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.UPDATE_GROUP_MEMBERS
    )

    update_group_members_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.UPDATE_GROUP_MEMBERS
    )

    response: Response = await async_client.put(
        url=RouterConfig.PREFIX + update_group_members_url_prefix + '1' + update_group_members_url_postfix,
        json=TestGroupMembersConfig().to_dict(to_lower=True),
        cookies=cookies
    )

    assert response.status_code == status.HTTP_200_OK
    group_data: Dict[str, Any] = response.json()
    assert len(group_data['members']) == 1


@pytest.mark.anyio
async def test_update_group_members_success_with_no_members(
        async_client: AsyncClient,
        create_test_group: None,
        cookies: Cookies
) -> None:

    update_group_members_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.UPDATE_GROUP_MEMBERS
    )

    update_group_members_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.UPDATE_GROUP_MEMBERS
    )

    response: Response = await async_client.put(
        url=RouterConfig.PREFIX + update_group_members_url_prefix + '1' + update_group_members_url_postfix,
        json={},
        cookies=cookies
    )

    assert response.status_code == status.HTTP_200_OK
    group_data: Dict[str, Any] = response.json()
    assert len(group_data['members']) == 0


@pytest.mark.anyio
async def test_update_group_members_fail_group_does_not_exist(
        async_client: AsyncClient,
        cookies: Cookies
) -> None:

    update_group_members_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.UPDATE_GROUP_MEMBERS
    )

    update_group_members_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.UPDATE_GROUP_MEMBERS
    )

    response: Response = await async_client.put(
        url=RouterConfig.PREFIX + update_group_members_url_prefix + '1' + update_group_members_url_postfix,
        json={},
        cookies=cookies
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert get_error_message_from_response(response=response) == ErrorDetails.GROUP_NOT_FOUND
