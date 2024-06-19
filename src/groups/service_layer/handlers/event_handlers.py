from src.groups.interfaces.handlers import GroupsEventHandler
from src.groups.domain.events import (
    GroupMembersInvitedEvent,
    GroupMembersAddedToGroupEvent
)


class SendAddToGroupNotificationsEventHandler(GroupsEventHandler):

    async def __call__(self, event: GroupMembersAddedToGroupEvent) -> None:
        # TODO should send notifications to added users
        pass


class SendRemoveFromGroupNotificationEventHandler(GroupsEventHandler):

    async def __call__(self, event: GroupMembersAddedToGroupEvent) -> None:
        # TODO should send notifications to added users
        pass


class SendRegisterMessageToInvitedUsersEventHandler(GroupsEventHandler):

    async def __call__(self, event: GroupMembersInvitedEvent) -> None:
        # TODO should send notifications for register to inveited users
        pass
