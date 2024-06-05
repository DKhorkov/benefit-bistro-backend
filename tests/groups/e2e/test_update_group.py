import pytest
from fastapi import status
from httpx import Response, AsyncClient, Cookies
from typing import Dict, Any

from src.core.utils import get_substring_before_chars, get_substring_after_chars
from src.groups.config import RouterConfig, URLPathsConfig
from src.groups.constants import ErrorDetails
from tests.utils import get_error_message_from_response
from tests.config import TestGroupConfig


@pytest.mark.anyio
async def test_update_group_success(
        async_client: AsyncClient,
        create_test_group: None,
        cookies: Cookies
) -> None:

    update_group_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.UPDATE_GROUP
    )

    update_group_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.UPDATE_GROUP
    )

    new_group_data = TestGroupConfig()
    new_group_data.NAME = 'SomeNewName'
    response: Response = await async_client.put(
        url=RouterConfig.PREFIX + update_group_url_prefix + '1' + update_group_url_postfix,
        json=new_group_data.to_dict(to_lower=True),
        cookies=cookies
    )

    assert response.status_code == status.HTTP_200_OK
    group_data: Dict[str, Any] = response.json()
    assert group_data['name'] == new_group_data.NAME


@pytest.mark.anyio
async def test_update_group_fail_group_does_not_exist(
        async_client: AsyncClient,
        cookies: Cookies
) -> None:

    update_group_url_prefix: str = get_substring_before_chars(
        chars='{',
        string=URLPathsConfig.UPDATE_GROUP
    )

    update_group_url_postfix: str = get_substring_after_chars(
        chars='}',
        string=URLPathsConfig.UPDATE_GROUP
    )

    response: Response = await async_client.put(
        url=RouterConfig.PREFIX + update_group_url_prefix + '1' + update_group_url_postfix,
        json=TestGroupConfig().to_dict(to_lower=True),
        cookies=cookies
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert get_error_message_from_response(response=response) == ErrorDetails.GROUP_NOT_FOUND
