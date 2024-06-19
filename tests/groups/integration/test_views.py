import pytest
from typing import List

from src.groups.domain.models import GroupModel
from src.groups.interfaces import GroupsRepository, GroupsUnitOfWork
from src.groups.service_layer.views import GroupsViews
from tests.config import FakeGroupConfig
from tests.groups.fake_objects import FakeGroupsUnitOfWork
from tests.groups.utils import create_fake_groups_repository_instance


@pytest.mark.anyio
async def test_groups_views_get_user_groups_with_existing_groups() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups: List[GroupModel] = await GroupsViews(uow=groups_unit_of_work).get_user_groups(user_id=1)
    assert len(groups) == 1
    group: GroupModel = groups[0]
    assert group.name == FakeGroupConfig.NAME
    assert group.owner_id == FakeGroupConfig.OWNER_ID


@pytest.mark.anyio
async def test_groups_views_get_user_groups_without_existing_groups() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups: List[GroupModel] = await GroupsViews(uow=groups_unit_of_work).get_user_groups(user_id=1)
    assert len(groups) == 0
