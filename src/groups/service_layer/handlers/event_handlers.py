from src.groups.interfaces.handlers import GroupEventHandler
from src.groups.domain.events import (
    GroupMembersInvitedEvent,
    GroupMembersAddedToGroupEvent
)


class GroupMembersAddedToGroupEventHandler(GroupEventHandler):

    async def __call__(self, event: GroupMembersAddedToGroupEvent) -> None:
        # TODO should send notifications to added users
        pass


class GroupMembersInvitedEventHandler(GroupEventHandler):

    async def __call__(self, event: GroupMembersInvitedEvent) -> None:
        # TODO should send notifications for register to inveited users
        pass
