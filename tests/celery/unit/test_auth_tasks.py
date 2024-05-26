import asyncio
from celery import Celery
from typing import Dict, Any

from src.users.models import UserModel
from src.celery.tasks.auth_tasks import send_verify_email_message
from tests.config import TestUserConfig


def test_send_verify_email_message_success(celery_app: Celery) -> None:
    user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True))
    user_data: Dict[str, Any] = asyncio.run(user.to_dict())
    assert send_verify_email_message.apply(kwargs={'user_data': user_data}).get() is None
