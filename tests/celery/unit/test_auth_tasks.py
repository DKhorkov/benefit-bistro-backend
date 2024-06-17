from celery import Celery
from src.celery.tasks.auth_tasks import send_verify_email_message
from tests.config import TestUserConfig


def test_send_verify_email_message_success(celery_app: Celery, create_test_user_if_not_exists: None) -> None:
    assert send_verify_email_message.apply(
        kwargs={
            'user_id': 1,
            'username': TestUserConfig.USERNAME,
            'email': TestUserConfig.EMAIL
        }
    ).get() is None
