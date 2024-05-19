import pytest
from typing import Sequence, Optional, List
from sqlalchemy import select, CursorResult, Row
from sqlalchemy.ext.asyncio import AsyncConnection

from src.auth.dependencies import register_user
from src.auth.schemas import RegisterUserScheme
from src.groups.exceptions import GroupAlreadyExistsError, GroupNotFoundError, GroupOwnerError
from src.groups.models import GroupModel
from src.auth.models import UserModel
from src.groups.schemas import CreateGroupScheme
from tests.config import TestUserConfig, TestGroupConfig
from src.groups.dependencies import (
    create_group,
    delete_group,
    get_current_user_groups
)


@pytest.mark.anyio
async def test_create_group_success(create_test_user_if_not_exists: None) -> None:
    group_data: CreateGroupScheme = CreateGroupScheme(**TestGroupConfig().to_dict(to_lower=True))
    user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True), id=1)
    group: GroupModel = await create_group(group_data=group_data, user=user)

    assert group.id == 1
    assert group.name == TestGroupConfig.NAME


@pytest.mark.anyio
async def test_create_group_fail_group_already_exists(create_test_group: None) -> None:
    group_data: CreateGroupScheme = CreateGroupScheme(**TestGroupConfig().to_dict(to_lower=True))
    user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True), id=1)
    with pytest.raises(GroupAlreadyExistsError):
        await create_group(group_data=group_data, user=user)


@pytest.mark.anyio
async def test_delete_group_success(create_test_group: None, async_connection: AsyncConnection) -> None:
    user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True), id=1)

    cursor: CursorResult = await async_connection.execute(select(GroupModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 1

    await delete_group(group_id=1, user=user)

    cursor = await async_connection.execute(select(GroupModel))
    result = cursor.all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_delete_group_fail_group_does_not_belong_to_current_user(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    second_user_config: TestUserConfig = TestUserConfig()
    second_user_config.EMAIL = 'secondUserEmail@gmail.com'
    second_user_config.USERNAME = 'secondUser'
    user_data: RegisterUserScheme = RegisterUserScheme(**second_user_config.to_dict(to_lower=True))
    user: UserModel = await register_user(user_data=user_data)

    user_cursor: CursorResult = await async_connection.execute(select(GroupModel))
    user_result: Optional[Row] = user_cursor.first()
    assert user_result

    with pytest.raises(GroupOwnerError):
        await delete_group(group_id=1, user=user)


@pytest.mark.anyio
async def test_delete_group_fail_group_does_not_exist(
        create_test_user_if_not_exists: None,
        async_connection: AsyncConnection
) -> None:

    user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True), id=1)
    with pytest.raises(GroupNotFoundError):
        await delete_group(group_id=1, user=user)


@pytest.mark.anyio
async def test_get_current_user_groups_success_with_no_existing_groups(create_test_user_if_not_exists: None) -> None:
    user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True), id=1)
    user_groups: List[GroupModel] = await get_current_user_groups(user=user)

    assert len(user_groups) == 0


@pytest.mark.anyio
async def test_get_current_user_groups_success_with_existing_groups(create_test_group: None) -> None:
    user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True), id=1)
    user_groups: List[GroupModel] = await get_current_user_groups(user=user)

    assert len(user_groups) == 1
    assert user_groups[0].name == TestGroupConfig.NAME
