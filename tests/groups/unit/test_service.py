import pytest
from typing import List

from src.groups.exceptions import GroupNotFoundError
from src.groups.interfaces.repositories import GroupsRepository
from src.groups.interfaces.units_of_work import GroupsUnitOfWork
from src.groups.domain.models import GroupModel, GroupMemberModel
from src.groups.service_layer.service import GroupsService
from tests.groups.fake_objects import FakeGroupsUnitOfWork, FakeGroupsRepository
from tests.config import FakeGroupConfig
from tests.groups.utils import create_fake_groups_repository_instance


@pytest.mark.anyio
async def test_groups_service_create_group_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 0
    group: GroupModel = GroupModel(**FakeGroupConfig().to_dict(to_lower=True))
    await groups_service.create_group(group=group)
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
async def test_groups_service_get_user_groups_success_with_no_groups() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 0
    user_groups: List[GroupModel] = await groups_service.get_user_groups(user_id=FakeGroupConfig.OWNER_ID)
    assert len(user_groups) == 0


@pytest.mark.anyio
async def test_groups_service_get_user_groups_success_with_groups() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    user_groups: List[GroupModel] = await groups_service.get_user_groups(user_id=FakeGroupConfig.OWNER_ID)
    assert len(user_groups) == 1
    group: GroupModel = user_groups[0]
    assert group.name == FakeGroupConfig.NAME
    assert group.owner_id == FakeGroupConfig.OWNER_ID


@pytest.mark.anyio
async def test_groups_service_get_group_by_id_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    found_group: GroupModel = await groups_service.get_group_by_id(id=1)
    assert found_group.name == FakeGroupConfig.NAME
    assert found_group.id == 1
    assert found_group.owner_id == FakeGroupConfig.OWNER_ID


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
    assert await groups_service.check_group_existence(owner_id=FakeGroupConfig.OWNER_ID, name=FakeGroupConfig.NAME)


@pytest.mark.anyio
async def test_groups_service_check_group_existence_fail_by_owner_id() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    assert not await groups_service.check_group_existence(owner_id=2, name=FakeGroupConfig.NAME)


@pytest.mark.anyio
async def test_groups_service_check_group_existence_fail_by_name() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    assert len(await groups_repository.list()) == 1
    assert not await groups_service.check_group_existence(owner_id=FakeGroupConfig.OWNER_ID, name='some_group_name')


@pytest.mark.anyio
async def test_groups_service_update_group_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)

    group_id: int = 1
    assert len(await groups_repository.list()) == 1
    group: GroupModel = await groups_service.get_group_by_id(id=group_id)
    assert group.name == FakeGroupConfig.NAME

    group.name = 'SomeNewName'
    group = await groups_service.update_group(id=group_id, group=group)
    assert not group.name == FakeGroupConfig.NAME


@pytest.mark.anyio
async def test_groups_service_update_group_fail_group_not_found() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)
    group: GroupModel = GroupModel(**FakeGroupConfig().to_dict(to_lower=True))

    with pytest.raises(GroupNotFoundError):
        await groups_service.update_group(id=1, group=group)


@pytest.mark.anyio
async def test_groups_service_add_group_members_success() -> None:
    group_id: int = 1
    user_id: int = 1

    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    assert isinstance(groups_repository, FakeGroupsRepository)
    assert len(groups_repository.groups) == 1
    assert len(groups_repository.groups[group_id].members) == 0

    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)
    group_member: GroupMemberModel = GroupMemberModel(group_id=group_id, user_id=user_id)
    group: GroupModel = await groups_service.add_group_members(id=group_id, members={group_member})

    assert len(groups_repository.groups[group_id].members) == 1
    assert group.members == {group_member}


@pytest.mark.anyio
async def test_groups_service_add_group_members_fail_group_not_found() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)
    with pytest.raises(GroupNotFoundError):
        await groups_service.add_group_members(id=1, members=set())


@pytest.mark.anyio
async def test_groups_service_remove_group_members_success() -> None:
    group_id: int = 1
    user_id: int = 1

    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    assert isinstance(groups_repository, FakeGroupsRepository)
    assert len(groups_repository.groups) == 1
    group_member: GroupMemberModel = GroupMemberModel(group_id=group_id, user_id=user_id)
    groups_repository.groups[group_id].members.add(group_member)
    assert len(groups_repository.groups[group_id].members) == 1

    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)
    group: GroupModel = await groups_service.remove_group_members(id=group_id, members={group_member})

    assert len(groups_repository.groups[group_id].members) == 0
    assert not group.members


@pytest.mark.anyio
async def test_groups_service_remove_group_members_fail_group_not_found() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)
    with pytest.raises(GroupNotFoundError):
        await groups_service.remove_group_members(id=1, members=set())


@pytest.mark.anyio
async def test_groups_service_remove_group_members_fail_no_member_in_group_members() -> None:
    group_id: int = 1

    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    groups_service: GroupsService = GroupsService(uow=groups_unit_of_work)
    group_member: GroupMemberModel = GroupMemberModel(group_id=group_id, user_id=1)
    with pytest.raises(KeyError):
        await groups_service.remove_group_members(id=group_id, members={group_member})
