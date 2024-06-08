from typing import Dict, List, Type
from queue import Queue

from src.core.exceptions import MessageBusMessageError
from src.core.interfaces import AbstractUnitOfWork
from src.core.interfaces.commands import AbstractCommand
from src.core.interfaces.events import AbstractEvent
from src.core.interfaces.handlers import AbstractEventHandler, AbstractCommandHandler
from src.core.interfaces.messages import Message


class MessageBus:

    def __init__(
        self,
        uow: AbstractUnitOfWork,
        event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]],
        command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler],
    ) -> None:

        self._uow = uow
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers
        self._queue: Queue = Queue()

    async def handle(self, message: Message) -> None:
        self._queue.put(message)
        while self._queue.not_empty:
            message = self._queue.get()
            if isinstance(message, AbstractEvent):
                await self._handle_event(event=message)
            elif isinstance(message, AbstractCommand):
                await self._handle_command(command=message)
            else:
                raise MessageBusMessageError

    async def _handle_event(self, event: AbstractEvent) -> None:
        handler: AbstractEventHandler
        for handler in self._event_handlers[type(event)]:
            await handler(event)
            for event in self._uow.events:
                self._queue.put_nowait(event)

    async def _handle_command(self, command: AbstractCommand) -> None:
        handler: AbstractCommandHandler = self._command_handlers[type(command)]
        await handler(command)
        for event in self._uow.events:
            self._queue.put_nowait(event)