from src.groups.domain.models import GroupModel
from src.groups.interfaces import GroupsRepository
from tests.config import FakeGroupConfig
from tests.groups.fake_objects import FakeGroupsRepository


def create_fake_groups_repository_instance(with_group: bool = False) -> GroupsRepository:
    groups_repository: GroupsRepository
    if with_group:
        group_id: int = 1
        group: GroupModel = GroupModel(**FakeGroupConfig().to_dict(to_lower=True), id=group_id)
        groups_repository = FakeGroupsRepository(groups={group_id: group})
    else:
        groups_repository = FakeGroupsRepository()

    return groups_repository
