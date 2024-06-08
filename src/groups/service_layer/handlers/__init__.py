from typing import List, Dict, Type

from src.core.interfaces.events import AbstractEvent
from src.core.interfaces.commands import AbstractCommand
from src.core.interfaces.handlers import AbstractEventHandler, AbstractCommandHandler
from src.groups.domain.events import (
    GroupMembersInvitedEvent,
    GroupMembersAddedToGroupEvent
)
from src.groups.domain.commands import (
    CreateGroupCommand,
    DeleteGroupCommand,
    UpdateGroupCommand,
    InviteGroupMembersCommand,
    AddGroupMembersCommand
)
from src.groups.service_layer.handlers.event_handlers import (
    GroupMembersAddedToGroupEventHandler
)
from src.groups.service_layer.handlers.command_handlers import (
    CreateGroupCommandHandler,
    DeleteGroupCommandHandler,
    UpdateGroupCommandHandler,
    AddGroupMembersCommandHandler
)


EVENTS_HANDLERS_RAW: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = {
    GroupMembersInvitedEvent: [],
    GroupMembersAddedToGroupEvent: [GroupMembersAddedToGroupEventHandler],
}

COMMANDS_HANDLERS_RAW: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]] = {
    CreateGroupCommand: CreateGroupCommandHandler,
    DeleteGroupCommand: DeleteGroupCommandHandler,
    UpdateGroupCommand: UpdateGroupCommandHandler,
    AddGroupMembersCommand: AddGroupMembersCommand,
}
