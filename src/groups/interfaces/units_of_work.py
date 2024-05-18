from abc import ABC

from src.groups.interfaces.repositories import GroupsRepository
from src.core.interfaces import AbstractUnitOfWork


class GroupsUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with groups, that is used by service layer of the groups module.
    The main goal is that implementations of this interface can be easily replaced in the service layer of
    the group module using dependency injection without disrupting its functionality.
    """

    groups: GroupsRepository
