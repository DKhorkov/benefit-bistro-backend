from dataclasses import dataclass
from typing import Set

from src.core.interfaces.events import AbstractEvent


@dataclass(frozen=True)
class GroupMembersAddedToGroupEvent(AbstractEvent):
    group_name: str
    group_members_usernames: Set[str]
    group_members_emails: Set[str]
    group_owner_username: str


@dataclass(frozen=True)
class GroupMembersRemovedFromGroupEvent(AbstractEvent):
    group_name: str
    group_members_usernames: Set[str]
    group_members_emails: Set[str]
    group_owner_username: str


@dataclass(frozen=True)
class GroupMembersInvitedEvent(AbstractEvent):
    group_name: str
    invited_group_members_emails: Set[str]
    group_owner_username: str
