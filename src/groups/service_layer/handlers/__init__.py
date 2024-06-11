from typing import List, Dict, Type

from src.core.interfaces.events import AbstractEvent
from src.core.interfaces.commands import AbstractCommand
from src.core.interfaces.handlers import AbstractEventHandler, AbstractCommandHandler
from src.groups.domain.events import (
    GroupMembersInvitedEvent,
    GroupMembersAddedToGroupEvent,
    GroupMembersRemovedFromGroupEvent
)
from src.groups.domain.commands import (
    CreateGroupCommand,
    DeleteGroupCommand,
    UpdateGroupCommand,
    InviteGroupMembersCommand,
    AddGroupMembersCommand,
    RemoveGroupMembersCommand,
)
from src.groups.service_layer.handlers.event_handlers import (
    GroupMembersAddedToGroupEventHandler,
    GroupMembersRemovedFromGroupEventHandler
)
from src.groups.service_layer.handlers.command_handlers import (
    CreateGroupCommandHandler,
    DeleteGroupCommandHandler,
    UpdateGroupCommandHandler,
    AddGroupMembersCommandHandler,
    RemoveGroupMembersCommandHandler,
)


EVENTS_HANDLERS_RAW: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = {
    GroupMembersInvitedEvent: [],
    GroupMembersAddedToGroupEvent: [GroupMembersAddedToGroupEventHandler],
    GroupMembersRemovedFromGroupEvent: [GroupMembersRemovedFromGroupEventHandler],
}

COMMANDS_HANDLERS_RAW: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]] = {
    CreateGroupCommand: CreateGroupCommandHandler,
    DeleteGroupCommand: DeleteGroupCommandHandler,
    UpdateGroupCommand: UpdateGroupCommandHandler,
    AddGroupMembersCommand: AddGroupMembersCommandHandler,
    RemoveGroupMembersCommand: RemoveGroupMembersCommandHandler,
}
