import pytest
from typing import List

from src.core.interfaces import AbstractEvent
from src.groups.domain.commands import (
    CreateGroupCommand,
    DeleteGroupCommand,
    UpdateGroupCommand,
    AddGroupMembersCommand,
    RemoveGroupMembersCommand
)
from src.groups.domain.events import (
    GroupMembersAddedToGroupEvent,
    GroupMembersRemovedFromGroupEvent
)
from src.groups.domain.models import GroupModel, GroupMemberModel
from src.groups.exceptions import (
    GroupOwnerError,
    GroupAlreadyExistsError
)
from src.groups.interfaces import GroupsRepository, GroupsUnitOfWork
from src.groups.service_layer.handlers.command_handlers import (
    UpdateGroupCommandHandler,
    DeleteGroupCommandHandler,
    CreateGroupCommandHandler,
    AddGroupMembersCommandHandler,
    RemoveGroupMembersCommandHandler
)
from src.users.domain.models import UserModel
from tests.config import FakeGroupConfig, FakeUserConfig
from tests.groups.fake_objects import FakeGroupsUnitOfWork, FakeGroupsRepository
from tests.groups.utils import create_fake_groups_repository_instance


@pytest.mark.anyio
async def test_create_group_command_handler_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance()
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: CreateGroupCommandHandler = CreateGroupCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=1, **FakeUserConfig().to_dict(to_lower=True))
    group: GroupModel = await handler(
        command=CreateGroupCommand(
            name=FakeGroupConfig.NAME,
            user=user
        )
    )

    assert group.name == FakeGroupConfig.NAME
    assert group.owner_id == FakeGroupConfig.OWNER_ID


@pytest.mark.anyio
async def test_create_group_command_handler_fail_group_already_exists() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: CreateGroupCommandHandler = CreateGroupCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=1, **FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(GroupAlreadyExistsError):
        await handler(
            command=CreateGroupCommand(
                name=FakeGroupConfig.NAME,
                user=user
            )
        )


@pytest.mark.anyio
async def test_delete_group_command_handler_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: DeleteGroupCommandHandler = DeleteGroupCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=1, **FakeUserConfig().to_dict(to_lower=True))
    await handler(
        command=DeleteGroupCommand(
            group_id=1,
            user=user
        )
    )


@pytest.mark.anyio
async def test_delete_group_command_handler_fail_group_does_not_belong_to_user() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: DeleteGroupCommandHandler = DeleteGroupCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=2, **FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(GroupOwnerError):
        await handler(
            command=DeleteGroupCommand(
                group_id=1,
                user=user
            )
        )


@pytest.mark.anyio
async def test_update_group_command_handler_success() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: UpdateGroupCommandHandler = UpdateGroupCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=1, **FakeUserConfig().to_dict(to_lower=True))
    new_name: str = 'some new group name'
    group: GroupModel = await handler(
        command=UpdateGroupCommand(
            group_id=1,
            user=user,
            name=new_name
        )
    )

    assert group.name == new_name
    assert group.owner_id == FakeGroupConfig.OWNER_ID


@pytest.mark.anyio
async def test_update_group_command_handler_fail_group_does_not_belong_to_user() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: UpdateGroupCommandHandler = UpdateGroupCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=2, **FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(GroupOwnerError):
        await handler(
            command=UpdateGroupCommand(
                group_id=1,
                user=user,
                name=FakeGroupConfig.NAME
            )
        )


@pytest.mark.anyio
async def test_add_group_members_command_handler_success() -> None:
    user_id: int = 1
    group_id: int = 1

    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    assert isinstance(groups_repository, FakeGroupsRepository)
    assert len(groups_repository.groups) == 1
    assert len(groups_repository.groups[group_id].members) == 0

    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: AddGroupMembersCommandHandler = AddGroupMembersCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=user_id, **FakeUserConfig().to_dict(to_lower=True))
    group: GroupModel = await handler(
        command=AddGroupMembersCommand(
            group_id=group_id,
            user=user,
            group_members={user}
        )
    )

    assert len(groups_repository.groups[group_id].members) == 1
    assert group.members == {GroupMemberModel(group_id=group_id, user_id=user_id)}

    events: List[AbstractEvent] = list(groups_unit_of_work.get_events())
    assert len(events) == 1
    assert isinstance(events[0], GroupMembersAddedToGroupEvent)


@pytest.mark.anyio
async def test_add_group_members_command_handler_fail_group_does_not_belong_to_user() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: AddGroupMembersCommandHandler = AddGroupMembersCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=2, **FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(GroupOwnerError):
        await handler(
            command=AddGroupMembersCommand(
                group_id=1,
                user=user,
                group_members={user}
            )
        )


@pytest.mark.anyio
async def test_remove_group_members_command_handler_success() -> None:
    user_id: int = 1
    group_id: int = 1

    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    assert isinstance(groups_repository, FakeGroupsRepository)
    assert len(groups_repository.groups) == 1
    groups_repository.groups[group_id].members.add(GroupMemberModel(group_id=group_id, user_id=user_id))
    assert len(groups_repository.groups[group_id].members) == 1

    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: RemoveGroupMembersCommandHandler = RemoveGroupMembersCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=user_id, **FakeUserConfig().to_dict(to_lower=True))
    group: GroupModel = await handler(
        command=RemoveGroupMembersCommand(
            group_id=group_id,
            user=user,
            group_members={user}
        )
    )

    assert len(groups_repository.groups[group_id].members) == 0
    assert not group.members

    events: List[AbstractEvent] = list(groups_unit_of_work.get_events())
    assert len(events) == 1
    assert isinstance(events[0], GroupMembersRemovedFromGroupEvent)


@pytest.mark.anyio
async def test_remove_group_members_command_handler_fail_group_does_not_belong_to_user() -> None:
    groups_repository: GroupsRepository = create_fake_groups_repository_instance(with_group=True)
    groups_unit_of_work: GroupsUnitOfWork = FakeGroupsUnitOfWork(groups_repository=groups_repository)
    handler: RemoveGroupMembersCommandHandler = RemoveGroupMembersCommandHandler(uow=groups_unit_of_work)
    user: UserModel = UserModel(id=2, **FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(GroupOwnerError):
        await handler(
            command=RemoveGroupMembersCommand(
                group_id=1,
                user=user,
                group_members={user}
            )
        )
