from src.users.interfaces.handlers import UsersEventHandler
from src.users.domain.events import (
    UserRegisteredEvent
)
from src.celery.tasks.users_tasks import send_verify_email_message


class SendVerifyEmailMessageEventHandler(UsersEventHandler):

    async def __call__(self, event: UserRegisteredEvent) -> None:
        send_verify_email_message.delay(**await event.to_dict())
