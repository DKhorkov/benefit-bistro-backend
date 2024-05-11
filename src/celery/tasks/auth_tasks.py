import asyncio
from typing import Dict, Any
from jinja2 import Template

from src.celery.celery_app import celery
from src.auth.models import UserModel
from src.celery.utils import send_email, get_email_template, create_message_object
from src.celery.config import PathsConfig, EmailSubjectsConfig
from src.core.utils import get_symbols_before_selected_symbol
from src.security.models import JWTDataModel
from src.security.utils import create_jwt_token
from src.config import links_config
from src.auth.config import (
    URLPathsConfig as AuthURLPathsConfig,
    RouterConfig as AuthRouterConfig
)


@celery.task
def send_verify_email_message(user_data: Dict[str, Any]) -> None:
    user: UserModel = UserModel(**user_data)
    template: Template = get_email_template(path=PathsConfig.VERIFY_EMAIL)
    jwt_data: JWTDataModel = JWTDataModel(user_id=user.id)
    token: str = asyncio.run(create_jwt_token(jwt_data=jwt_data))
    verify_email_path: str = AuthRouterConfig.PREFIX + get_symbols_before_selected_symbol(
        symbol='{',
        string=AuthURLPathsConfig.VERIFY_EMAIL
    )

    link: str = f'{links_config.HTTP_PROTOCOL}://{links_config.DOMAIN}{verify_email_path}{token}'
    text: str = template.render(
        data={
            'username': user.username,
            'link': link,
        }
    )

    message: str = create_message_object(text=text, subject=EmailSubjectsConfig.VERIFY_EMAIL, email_to=user.email)
    send_email(to_addrs=user.email, message=message)
