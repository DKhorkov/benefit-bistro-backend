from src.groups.domain.events import GroupMembersAddedToGroupEvent
from src.groups.interfaces.handlers import GroupEventHandler
from src.groups.domain.events import (
    GroupMembersInvitedEvent,
    GroupMembersAddedToGroupEvent
)


class GroupMembersAddedToGroupEventHandler(GroupEventHandler):

    async def __call__(self, event: GroupMembersAddedToGroupEvent) -> None:
        # TODO should send notifications to added users
        pass
