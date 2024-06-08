from typing import Dict, Optional, List

from src.groups.interfaces.units_of_work import GroupsUnitOfWork
from src.groups.interfaces.repositories import GroupsRepository
from src.groups.domain.models import GroupModel
from src.core.interfaces import AbstractModel


class FakeGroupsRepository(GroupsRepository):

    def __init__(self, groups: Optional[Dict[int, GroupModel]] = None) -> None:
        self.groups: Dict[int, GroupModel] = groups if groups else {}

    async def get(self, id: int) -> Optional[GroupModel]:
        return self.groups.get(id)

    async def get_owner_groups(self, owner_id: int) -> List[GroupModel]:
        return [group for group in self.groups.values() if group.id == owner_id]

    async def get_by_owner_and_name(self, name: str, owner_id: int) -> Optional[GroupModel]:
        for group in self.groups.values():
            if group.id == owner_id and group.name == name:
                return group

        return None

    async def add(self, model: AbstractModel) -> GroupModel:
        group: GroupModel = GroupModel(**await model.to_dict())
        self.groups[group.id] = group
        return group

    async def update(self, id: int, model: AbstractModel) -> GroupModel:
        group: GroupModel = GroupModel(**await model.to_dict())
        if id in self.groups:
            self.groups[id] = group

        return group

    async def delete(self, id: int) -> None:
        if id in self.groups:
            del self.groups[id]

    async def list(self) -> List[GroupModel]:
        return list(self.groups.values())


class FakeGroupsUnitOfWork(GroupsUnitOfWork):

    def __init__(self, groups_repository: GroupsRepository) -> None:
        self.groups: GroupsRepository = groups_repository
        self.committed: bool = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass
