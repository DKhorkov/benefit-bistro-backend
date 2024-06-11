from typing import List, Set
from fastapi import Depends

from src.core.interfaces import AbstractBootstrap
from src.core.messagebus import MessageBus
from src.groups.domain.commands import (
    CreateGroupCommand,
    DeleteGroupCommand,
    UpdateGroupCommand
)
from src.groups.entypoints.bootstraps import GroupsBootstrap
from src.groups.domain.models import GroupModel, GroupMemberModel
from src.groups.entypoints.schemas import CreateOrUpdateGroupScheme, UpdateGroupMembersScheme
from src.groups.service_layer.units_of_work import SQLAlchemyGroupsUnitOfWork
from src.groups.service_layer.views import GroupsViews
from src.users.models import UserModel
from src.users.dependencies import authenticate_user


"""
Can not user Bootstrap object in dependencies, so its defined in each dependency body.
"""


async def create_group(
        group_data: CreateOrUpdateGroupScheme,
        user: UserModel = Depends(authenticate_user)
) -> GroupModel:

    bootstrap: AbstractBootstrap = GroupsBootstrap(uow=SQLAlchemyGroupsUnitOfWork())
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(
        CreateGroupCommand(
            user=user,
            **group_data.model_dump()
        )
    )

    return messagebus.command_result


async def delete_group(group_id: int, user: UserModel = Depends(authenticate_user)) -> None:
    bootstrap: AbstractBootstrap = GroupsBootstrap(uow=SQLAlchemyGroupsUnitOfWork())
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(
        DeleteGroupCommand(
            user=user,
            group_id=group_id
        )
    )


async def get_current_user_groups(user: UserModel = Depends(authenticate_user)) -> List[GroupModel]:
    groups_views: GroupsViews = GroupsViews(uow=SQLAlchemyGroupsUnitOfWork())
    return await groups_views.get_user_groups(user_id=user.id)


async def update_group(
        group_data: CreateOrUpdateGroupScheme,
        group_id: int,
        user: UserModel = Depends(authenticate_user)
) -> GroupModel:

    bootstrap: AbstractBootstrap = GroupsBootstrap(uow=SQLAlchemyGroupsUnitOfWork())
    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(
        UpdateGroupCommand(
            user=user,
            group_id=group_id,
            **group_data.model_dump()
        )
    )

    return messagebus.command_result
