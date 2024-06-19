import pytest
from fastapi import status
from httpx import Response, AsyncClient, Cookies
from typing import Dict, Any

from src.groups.config import RouterConfig, URLPathsConfig, GroupValidationConfig
from src.groups.constants import ErrorDetails
from src.groups.domain.models import GroupModel
from tests.utils import get_error_message_from_response, generate_random_string
from tests.config import FakeGroupConfig


@pytest.mark.anyio
async def test_create_group_success(
        async_client: AsyncClient,
        create_test_user_if_not_exists: None,
        cookies: Cookies
) -> None:

    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.CREATE_GROUP,
        json=FakeGroupConfig().to_dict(to_lower=True),
        cookies=cookies
    )

    assert response.status_code == status.HTTP_201_CREATED
    group_data: Dict[str, Any] = response.json()
    group_data.pop('members')
    group: GroupModel = GroupModel(**group_data)
    assert group.name == FakeGroupConfig.NAME


@pytest.mark.anyio
async def test_create_group_fail_user_unauthorized(
        async_client: AsyncClient,
        create_test_user_if_not_exists: None
) -> None:

    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.CREATE_GROUP,
        json=FakeGroupConfig().to_dict(to_lower=True)
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_group_fail_group_already_exists(
        async_client: AsyncClient,
        create_test_group: None,
        cookies: Cookies
) -> None:

    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.CREATE_GROUP,
        json=FakeGroupConfig().to_dict(to_lower=True),
        cookies=cookies
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert get_error_message_from_response(response=response) == ErrorDetails.GROUP_ALREADY_EXISTS


@pytest.mark.anyio
async def test_create_group_fail_group_name_too_short(
        async_client: AsyncClient,
        create_test_user_if_not_exists: None,
        cookies: Cookies
) -> None:

    test_group_config: FakeGroupConfig = FakeGroupConfig()
    test_group_config.NAME = generate_random_string(GroupValidationConfig.NAME_MIN_LENGTH - 1)
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.CREATE_GROUP,
        json=test_group_config.to_dict(to_lower=True),
        cookies=cookies
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.GROUP_NAME_VALIDATION_ERROR


@pytest.mark.anyio
async def test_create_group_fail_group_name_too_long(
        async_client: AsyncClient,
        create_test_user_if_not_exists: None,
        cookies: Cookies
) -> None:

    test_group_config: FakeGroupConfig = FakeGroupConfig()
    test_group_config.NAME = generate_random_string(GroupValidationConfig.NAME_MAX_LENGTH + 1)
    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.CREATE_GROUP,
        json=test_group_config.to_dict(to_lower=True),
        cookies=cookies
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert get_error_message_from_response(response=response) == ErrorDetails.GROUP_NAME_VALIDATION_ERROR
