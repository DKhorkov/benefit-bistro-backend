from typing import List
from fastapi import Depends

from src.core.bootstrap import Bootstrap
from src.core.messagebus import MessageBus
from src.groups.domain.commands import (
    CreateGroupCommand,
    DeleteGroupCommand,
    UpdateGroupCommand
)
from src.groups.domain.models import GroupModel
from src.groups.entypoints.schemas import CreateOrUpdateGroupScheme
from src.groups.service_layer.units_of_work import SQLAlchemyGroupsUnitOfWork
from src.groups.service_layer.handlers import EVENTS_HANDLERS_FOR_INJECTION, COMMANDS_HANDLERS_FOR_INJECTION
from src.groups.service_layer.views import GroupsViews
from src.users.domain.models import UserModel
from src.users.entrypoints.dependencies import authenticate_user


"""
Can not use Bootstrap object in dependencies, so its defined in each dependency body.
"""


async def create_group(
        group_data: CreateOrUpdateGroupScheme,
        user: UserModel = Depends(authenticate_user)
) -> GroupModel:

    bootstrap: Bootstrap = Bootstrap(
        uow=SQLAlchemyGroupsUnitOfWork(),
        events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
        commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
    )

    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(
        CreateGroupCommand(
            user=user,
            **group_data.model_dump()
        )
    )

    return messagebus.command_result


async def delete_group(group_id: int, user: UserModel = Depends(authenticate_user)) -> None:
    bootstrap: Bootstrap = Bootstrap(
        uow=SQLAlchemyGroupsUnitOfWork(),
        events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
        commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
    )

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

    bootstrap: Bootstrap = Bootstrap(
        uow=SQLAlchemyGroupsUnitOfWork(),
        events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
        commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
    )

    messagebus: MessageBus = await bootstrap.get_messagebus()
    await messagebus.handle(
        UpdateGroupCommand(
            user=user,
            group_id=group_id,
            **group_data.model_dump()
        )
    )

    return messagebus.command_result
