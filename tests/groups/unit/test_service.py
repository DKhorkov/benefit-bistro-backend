import pytest
from typing import List

from src.groups.exceptions import GroupNotFoundError
from src.groups.interfaces.repositories import GroupsRepository
from src.groups.interfaces.units_of_work import GroupsUnitOfWork
from src.groups.models import GroupModel
from src.groups.schemas import CreateGroupScheme
from src.groups.service import GroupsService
from tests.groups.fake_objects import FakeGroupsRepository, FakeGroupsUnitOfWork
from tests.config import TestGroupConfig


def create_fake_groups_repository_instance(with_group: bool = False) -> GroupsRepository:
    groups_repository: GroupsRepository
    if with_group:
        group_id: int = 1
        group: GroupModel = GroupModel(**TestGroupConfig().to_dict(to_lower=True), id=group_id)
        groups_repository = FakeGroupsRepository(groups={group_id: group})
    else:
        groups_repository = FakeGroupsRepository()

    return groups_repository


@pytest.mark.anyio
async def test_groups_service_create_group_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 0
    group_data: CreateGroupScheme = CreateGroupScheme(**TestGroupConfig().to_dict(to_lower=True))
    await groups_service.create_group(group_data=group_data)
    assert len(await groups_repository.list()) == 1


@pytest.mark.anyio
async def test_groups_service_delete_group_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    await groups_service.delete_group(id=1)
    assert len(await groups_repository.list()) == 0


@pytest.mark.anyio
async def test_groups_service_get_owner_groups_success_with_no_groups() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 0
    user_groups: List[GroupModel] = await groups_service.get_owner_groups(owner_id=TestGroupConfig.OWNER_ID)
    assert len(user_groups) == 0


@pytest.mark.anyio
async def test_groups_service_get_owner_groups_success_with_groups() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    user_groups: List[GroupModel] = await groups_service.get_owner_groups(owner_id=TestGroupConfig.OWNER_ID)
    assert len(user_groups) == 1
    group: GroupModel = user_groups[0]
    assert group.name == TestGroupConfig.NAME
    assert group.owner_id == TestGroupConfig.OWNER_ID


@pytest.mark.anyio
async def test_groups_service_get_group_by_id_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    found_group: GroupModel = await groups_service.get_group_by_id(id=1)
    assert found_group.name == TestGroupConfig.NAME
    assert found_group.id == 1
    assert found_group.owner_id == TestGroupConfig.OWNER_ID


@pytest.mark.anyio
async def test_groups_service_get_group_by_id_fail() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 0
    with pytest.raises(GroupNotFoundError):
        await groups_service.get_group_by_id(id=1)


@pytest.mark.anyio
async def test_groups_service_check_group_existence_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    assert await groups_service.check_group_existence(owner_id=TestGroupConfig.OWNER_ID, name=TestGroupConfig.NAME)


@pytest.mark.anyio
async def test_groups_service_check_group_existence_fail_by_owner_id() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    assert not await groups_service.check_group_existence(owner_id=2, name=TestGroupConfig.NAME)


@pytest.mark.anyio
async def test_groups_service_check_group_existence_fail_by_name() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    assert not await groups_service.check_group_existence(owner_id=TestGroupConfig.OWNER_ID, name='some_group_name')
