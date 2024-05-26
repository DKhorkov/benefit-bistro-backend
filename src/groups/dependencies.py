from typing import List
from fastapi import Depends

from src.groups.exceptions import GroupAlreadyExistsError, GroupOwnerError
from src.groups.models import GroupModel
from src.groups.schemas import CreateGroupScheme
from src.groups.service import GroupsService
from src.groups.units_of_work import SQLAlchemyGroupsUnitOfWork
from src.users.models import UserModel
from src.users.dependencies import authenticate_user


async def create_group(group_data: CreateGroupScheme, user: UserModel = Depends(authenticate_user)) -> GroupModel:
    """
    Creates a new group for current user, if user doesn't have group with same name.
    """

    group_service: GroupsService = GroupsService(uow=SQLAlchemyGroupsUnitOfWork())
    if await group_service.check_group_existence(name=group_data.name, owner_id=user.id):
        raise GroupAlreadyExistsError

    group_data.owner_id = user.id
    return await group_service.create_group(group_data=group_data)


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
    groups: List[GroupModel] = await group_service.get_owner_groups(owner_id=user.id)
    return groups
