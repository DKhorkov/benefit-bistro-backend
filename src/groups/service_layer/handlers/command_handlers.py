from typing import Set

from src.groups.domain.events import GroupMembersAddedToGroupEvent
from src.groups.interfaces.handlers import GroupCommandHandler
from src.groups.domain.commands import (
    CreateGroupCommand,
    DeleteGroupCommand,
    UpdateGroupCommand,
    AddGroupMembersCommand
)
from src.groups.domain.models import GroupModel, GroupMemberModel
from src.groups.exceptions import GroupAlreadyExistsError, GroupOwnerError
from src.groups.service_layer.service import GroupsService


class CreateGroupCommandHandler(GroupCommandHandler):

    async def __call__(self, command: CreateGroupCommand) -> None:
        """
        Creates a new group for current user, if user doesn't have group with same name.
        """

        groups_service: GroupsService = GroupsService(uow=self._uow)
        if groups_service.check_group_existence(name=command.group_name, owner_id=command.user.id):
            raise GroupAlreadyExistsError

        group: GroupModel = GroupModel(**await command.to_dict(exclude={'user'}))
        await groups_service.create_group(group=group)


class DeleteGroupCommandHandler(GroupCommandHandler):

    async def __call__(self, command: DeleteGroupCommand) -> None:
        """
        Deletes group, if group belongs to current user.
        """

        groups_service: GroupsService = GroupsService(uow=self._uow)
        group: GroupModel = await groups_service.get_group_by_id(id=command.group_id)
        if not group.owner_id == command.user.id:
            raise GroupOwnerError

        await groups_service.delete_group(id=command.group_id)


class UpdateGroupCommandHandler(GroupCommandHandler):

    async def __call__(self, command: UpdateGroupCommand) -> None:
        """
        Updates group info, if group belongs to current user.
        """

        groups_service: GroupsService = GroupsService(uow=self._uow)
        group: GroupModel = await groups_service.get_group_by_id(id=command.group_id)
        if not group.owner_id == command.user.id:
            raise GroupOwnerError

        # Excluding all relationships to avoid SQLAlchemy errors:
        group = GroupModel(
            **await group.to_dict(exclude={'members'}) | await command.to_dict(exclude={'group_id', 'user'})
        )
        await groups_service.update_group(id=command.group_id, group=group)


class AddGroupMembersCommandHandler(GroupCommandHandler):

    async def __call__(self, command: AddGroupMembersCommand) -> None:
        """
        Updates group members, if group belongs to current user, and creates event signaling that operation
        was successfully executed.
        """

        async with self._uow as uow:
            groups_service: GroupsService = GroupsService(uow=uow)
            group: GroupModel = await groups_service.get_group_by_id(id=command.group_id)
            if not group.owner_id == command.user.id:
                raise GroupOwnerError

            group_members: Set[GroupMemberModel] = {
                GroupMemberModel(
                    group_id=group.id,
                    user_id=group_member.id,
                ) for group_member in command.group_members
            }

            await groups_service.add_group_members(id=group.id, members=group_members)
            uow.events.append(
                GroupMembersAddedToGroupEvent(
                    group_name=group.name,
                    group_owner_username=command.user.username,
                    group_members_emails=[group_member.email for group_member in command.group_members],
                    group_members_usernames=[group_member.username for group_member in command.group_members]
                )
            )
