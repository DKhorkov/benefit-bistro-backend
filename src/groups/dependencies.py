from typing import List, Set
from fastapi import Depends

from src.groups.exceptions import GroupAlreadyExistsError, GroupOwnerError
from src.groups.models import GroupModel, GroupMemberModel
from src.groups.schemas import CreateOrUpdateGroupScheme, UpdateGroupMembersScheme
from src.groups.service import GroupsService
from src.groups.units_of_work import SQLAlchemyGroupsUnitOfWork
from src.users.models import UserModel
from src.users.dependencies import authenticate_user


async def create_group(
        group_data: CreateOrUpdateGroupScheme,
        user: UserModel = Depends(authenticate_user)
) -> GroupModel:

    """
    Creates a new group for current user, if user doesn't have group with same name.
    """

    group_service: GroupsService = GroupsService(uow=SQLAlchemyGroupsUnitOfWork())
    if await group_service.check_group_existence(name=group_data.name, owner_id=user.id):
        raise GroupAlreadyExistsError

    group: GroupModel = GroupModel(**group_data.model_dump(), owner_id=user.id)
    return await group_service.create_group(group=group)


async def delete_group(group_id: int, user: UserModel = Depends(authenticate_user)) -> None:
    """
    Deletes group, if group belongs to current user.
    """

    group_service: GroupsService = GroupsService(uow=SQLAlchemyGroupsUnitOfWork())
    group: GroupModel = await group_service.get_group_by_id(id=group_id)
    if not group.owner_id == user.id:
        raise GroupOwnerError

    await group_service.delete_group(id=group_id)


async def get_current_user_groups(user: UserModel = Depends(authenticate_user)) -> List[GroupModel]:
    """
    Provides a list of groups, belonging to current user.
    """

    group_service: GroupsService = GroupsService(uow=SQLAlchemyGroupsUnitOfWork())
    return await group_service.get_owner_groups(owner_id=user.id)


async def update_group_members(
        group_members_data: UpdateGroupMembersScheme,
        group_id: int,
        user: UserModel = Depends(authenticate_user)
) -> GroupModel:

    group_service: GroupsService = GroupsService(uow=SQLAlchemyGroupsUnitOfWork())
    group: GroupModel = await group_service.get_group_by_id(id=group_id)
    if not group.owner_id == user.id:
        raise GroupOwnerError

    group_members: Set[GroupMemberModel] = {
        GroupMemberModel(
            group_id=group_id,
            user_id=group_member_id,
        ) for group_member_id in group_members_data.group_member_ids
    }

    return await group_service.update_group_members(id=group_id, members=group_members)


async def update_group(
        group_data: CreateOrUpdateGroupScheme,
        group_id: int,
        user: UserModel = Depends(authenticate_user)
):

    group_service: GroupsService = GroupsService(uow=SQLAlchemyGroupsUnitOfWork())
    group: GroupModel = await group_service.get_group_by_id(id=group_id)
    if not group.owner_id == user.id:
        raise GroupOwnerError

    # Excluding all relationships to avoid SQLAlchemy errors:
    group = GroupModel(**await group.to_dict(exclude={'members'}) | group_data.model_dump())
    return await group_service.update_group(id=group_id, group=group)
