from dataclasses import dataclass, field
from typing import Set

from src.core.interfaces import AbstractModel


@dataclass
class GroupMemberModel(AbstractModel):
    group_id: int
    user_id: int

    def __hash__(self) -> int:
        return hash(f'{self.group_id}_{self.user_id}')


@dataclass
class GroupModel(AbstractModel):
    name: str
    owner_id: int

    # Optional args:
    id: int = 0

    members: Set[GroupMemberModel] = field(default_factory=set)
