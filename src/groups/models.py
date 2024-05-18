from dataclasses import dataclass

from src.core.interfaces import AbstractModel


@dataclass
class GroupModel(AbstractModel):
    name: str
    owner_id: int

    # Optional args:
    id: int = 0
