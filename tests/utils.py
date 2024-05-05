import os
from random import choice
from string import ascii_uppercase
from typing import Dict, Any
from httpx import Response

from src.core.database.config import database_config


def get_base_url() -> str:
    host: str = os.environ.get('HOST')
    port: str = os.environ.get('PORT')
    return f'http://{host}:{port}'


def drop_test_db() -> None:
    if os.path.exists(database_config.DATABASE_NAME):
        os.remove(database_config.DATABASE_NAME)


def get_error_message_from_response(response: Response) -> str:
    response_content: Dict[str, Any] = response.json()
    try:
        return response_content['detail'][0]['msg']
    except TypeError:
        return response_content['detail']


def generate_random_string(length: int) -> str:
    return ''.join(choice(ascii_uppercase) for _ in range(length))
