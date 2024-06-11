import inspect
from types import MappingProxyType
from typing import Union, Type, Dict, Any
from abc import ABC, abstractmethod

from src.core.interfaces.handlers import AbstractEventHandler, AbstractCommandHandler
from src.core.interfaces.units_of_work import AbstractUnitOfWork
from src.core.messagebus import MessageBus


class AbstractBootstrap(ABC):
    """
    Abstract Bootstrap class for Dependencies Injection purposes.
    """

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow: AbstractUnitOfWork = uow

    @abstractmethod
    async def get_messagebus(self) -> MessageBus:
        raise NotImplementedError

    @staticmethod
    async def _inject_dependencies(
            handler: Union[Type[AbstractEventHandler], Type[AbstractCommandHandler]],
            dependencies: Dict[str, Any]
    ) -> Union[AbstractEventHandler, AbstractCommandHandler]:

        """
        Inspecting handler to know its signature and init params, after which only necessary dependencies will be
        injected to the handler.
        """

        params: MappingProxyType[str, inspect.Parameter] = inspect.signature(handler).parameters
        handler_dependencies: Dict[str, Any] = {
            name: dependency
            for name, dependency in dependencies.items()
            if name in params
        }
        return handler(**handler_dependencies)
