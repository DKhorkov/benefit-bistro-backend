from dataclasses import dataclass
from typing import List

from src.core.interfaces.commands import AbstractCommand
from src.users.models import UserModel


@dataclass(frozen=True)
class CreateGroupCommand(AbstractCommand):
    group_name: str
    user: UserModel


@dataclass(frozen=True)
class DeleteGroupCommand(AbstractCommand):
    group_id: int
    user: UserModel


@dataclass(frozen=True)
class UpdateGroupCommand(AbstractCommand):
    group_id: int
    user: UserModel
    group_name: str


@dataclass(frozen=True)
class AddGroupMembersCommand(AbstractCommand):
    group_id: int
    user: UserModel
    group_members: List[UserModel]


@dataclass(frozen=True)
class InviteGroupMembersCommand(AbstractCommand):
    group_id: int
    user: UserModel
    invited_group_members_emails: List[str]
