from typing import List, Dict, Type

from src.core.interfaces.events import AbstractEvent
from src.core.interfaces.commands import AbstractCommand
from src.core.interfaces.handlers import AbstractEventHandler, AbstractCommandHandler
from src.users.domain.events import (
    UserRegisteredEvent
)
from src.users.domain.commands import (
    RegisterUserCommand,
    VerifyUserEmailCommand,
    VerifyUserCredentialsCommand,
    GetUserCommand,
)
from src.users.service_layer.handlers.event_handlers import (
    SendVerifyEmailMessageEventHandler,
)
from src.users.service_layer.handlers.command_handlers import (
    RegisterUserCommandHandler,
    VerifyUserCredentialsCommandHandler,
    VerifyUserEmailCommandHandler,
    GetUserCommandHandler,
)


EVENTS_HANDLERS_FOR_INJECTION: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = {
    UserRegisteredEvent: [SendVerifyEmailMessageEventHandler],
}

COMMANDS_HANDLERS_FOR_INJECTION: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]] = {
    RegisterUserCommand: RegisterUserCommandHandler,
    VerifyUserEmailCommand: VerifyUserEmailCommandHandler,
    VerifyUserCredentialsCommand: VerifyUserCredentialsCommandHandler,
    GetUserCommand: GetUserCommandHandler,
}
