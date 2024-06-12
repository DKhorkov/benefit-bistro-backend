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
    SendRegisterMessageToInvitedUsersEventHandler,
    SendAddToGroupNotificationsEventHandler,
    SendRemoveFromGroupNotificationEventHandler
)
from src.groups.service_layer.handlers.command_handlers import (
    CreateGroupCommandHandler,
    DeleteGroupCommandHandler,
    UpdateGroupCommandHandler,
    AddGroupMembersCommandHandler,
    RemoveGroupMembersCommandHandler,
)


EVENTS_HANDLERS_FOR_INJECTION: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = {
    GroupMembersInvitedEvent: [SendRegisterMessageToInvitedUsersEventHandler],
    GroupMembersAddedToGroupEvent: [SendAddToGroupNotificationsEventHandler],
    GroupMembersRemovedFromGroupEvent: [SendRemoveFromGroupNotificationEventHandler],
}

COMMANDS_HANDLERS_FOR_INJECTION: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]] = {
    CreateGroupCommand: CreateGroupCommandHandler,
    DeleteGroupCommand: DeleteGroupCommandHandler,
    UpdateGroupCommand: UpdateGroupCommandHandler,
    AddGroupMembersCommand: AddGroupMembersCommandHandler,
    RemoveGroupMembersCommand: RemoveGroupMembersCommandHandler,
}
