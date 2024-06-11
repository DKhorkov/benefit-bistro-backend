from typing import Dict, Any, Type, List

from src.core.interfaces import AbstractBootstrap, AbstractCommand, AbstractEvent
from src.core.interfaces.handlers import AbstractCommandHandler, AbstractEventHandler
from src.core.messagebus import MessageBus
from src.groups.service_layer.handlers import EVENTS_HANDLERS_RAW, COMMANDS_HANDLERS_RAW


class GroupsBootstrap(AbstractBootstrap):

    async def get_messagebus(self) -> MessageBus:
        dependencies: Dict[str, Any] = {'uow': self._uow}
        injected_event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]] = {
            event_type: [
                await self._inject_dependencies(handler=handler, dependencies=dependencies)
                for handler in event_handlers
            ]
            for event_type, event_handlers in EVENTS_HANDLERS_RAW.items()
        }

        injected_command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler] = {
            command_type: await self._inject_dependencies(handler=handler, dependencies=dependencies)
            for command_type, handler in COMMANDS_HANDLERS_RAW.items()
        }

        return MessageBus(
            uow=self._uow,
            event_handlers=injected_event_handlers,
            command_handlers=injected_command_handlers,
        )
