from typing import List

from src.groups.domain.models import GroupModel
from src.groups.interfaces.units_of_work import GroupsUnitOfWork
from src.groups.service_layer.service import GroupsService


class GroupViews:
    """
    Views related to groups, which purpose is to return information upon read requests,
    due to the fact that write requests (represented by commands) are different from read requests.

    # TODO At current moment uses repositories pattern to retrieve data. In future can be changed on raw SQL
    # TODO for speed-up purpose
    """

    def __init__(self, uow: GroupsUnitOfWork) -> None:
        self._uow: GroupsUnitOfWork = uow

    async def get_user_groups(self, user_id: int) -> List[GroupModel]:
        """
        Provides a list of groups, belonging to current user.
        """

        groups_service: GroupsService = GroupsService(self._uow)
        return await groups_service.get_user_groups(user_id=user_id)
