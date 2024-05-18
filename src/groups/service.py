from typing import Optional, List

from src.groups.models import GroupModel
from src.groups.schemas import CreateGroupScheme
from src.groups.interfaces.units_of_work import GroupsUnitOfWork
from src.groups.exceptions import GroupNotFoundError


class GroupsService:
    """
    Service layer according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, uow: GroupsUnitOfWork) -> None:
        self._uow: GroupsUnitOfWork = uow

    async def get_group_by_id(self, id: int) -> GroupModel:
        async with self._uow as uow:
            group: Optional[GroupModel] = await uow.groups.get(id=id)
            if not group:
                raise GroupNotFoundError

            return group

    async def create_group(self, group_data: CreateGroupScheme) -> GroupModel:
        async with self._uow as uow:
            group: GroupModel = await uow.groups.add(GroupModel(**group_data.model_dump()))
            await uow.commit()
            return group

    async def check_group_existence(self, owner_id: int, name: str) -> bool:
        async with self._uow as uow:
            group: Optional[GroupModel] = await uow.groups.get_group_by_owner_and_name(name=name, owner_id=owner_id)
            if group:
                return True

        return False

    async def delete_group(self, id: int) -> None:
        async with self._uow as uow:
            await uow.groups.delete(id=id)
            await uow.commit()

    async def get_owner_groups(self, owner_id: int) -> List[GroupModel]:
        async with self._uow as uow:
            groups: List[GroupModel] = await uow.groups.get_owner_groups(owner_id=owner_id)
            return groups
