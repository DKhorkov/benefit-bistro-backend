from dataclasses import dataclass
from typing import Set

from src.core.interfaces.commands import AbstractCommand
from src.users.domain.models import UserModel


@dataclass(frozen=True)
class CreateGroupCommand(AbstractCommand):
    name: str
    user: UserModel


@dataclass(frozen=True)
class DeleteGroupCommand(AbstractCommand):
    group_id: int
    user: UserModel


@dataclass(frozen=True)
class UpdateGroupCommand(AbstractCommand):
    group_id: int
    user: UserModel
    name: str


@dataclass(frozen=True)
class AddGroupMembersCommand(AbstractCommand):
    group_id: int
    user: UserModel
    group_members: Set[UserModel]


@dataclass(frozen=True)
class RemoveGroupMembersCommand(AbstractCommand):
    group_id: int
    user: UserModel
    group_members: Set[UserModel]


@dataclass(frozen=True)
class InviteGroupMembersCommand(AbstractCommand):
    group_id: int
    user: UserModel
    invited_group_members_emails: Set[str]
