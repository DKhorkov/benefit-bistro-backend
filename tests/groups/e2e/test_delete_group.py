import os

import pytest
from fastapi import status
from httpx import Response, AsyncClient, Cookies
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.users.config import cookies_config
from src.users.models import UserModel
from src.users.utils import hash_password
from src.core.database.connection import DATABASE_URL
from src.core.utils import get_symbols_before_selected_symbol
from src.groups.config import RouterConfig, URLPathsConfig
from src.users.config import (
    URLPathsConfig as UsersURLPathsConfig,
    RouterConfig as UsersRouterConfig
)
from tests.config import TestUserConfig


@pytest.mark.anyio
async def test_delete_group_success(
        async_client: AsyncClient,
        create_test_group: None,
        cookies: Cookies
) -> None:

    delete_group_url_base: str = get_symbols_before_selected_symbol(
        symbol='{',
        string=URLPathsConfig.DELETE_GROUP
    )

    response: Response = await async_client.delete(
        url=RouterConfig.PREFIX + delete_group_url_base + '1',
        cookies=cookies
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_delete_group_fail_group_does_not_exist(
        async_client: AsyncClient,
        create_test_user_if_not_exists: None,
        cookies: Cookies
) -> None:

    delete_group_url_base: str = get_symbols_before_selected_symbol(
        symbol='{',
        string=URLPathsConfig.DELETE_GROUP
    )

    response: Response = await async_client.delete(
        url=RouterConfig.PREFIX + delete_group_url_base + '1',
        cookies=cookies
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_delete_group_fail_group_does_not_belong_to_current_user(
        async_client: AsyncClient,
        create_test_group: None,
) -> None:

    second_user_email: str = 'someNewEmail@gmail.com'
    second_user_username: str = 'someNewUsername'
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    test_user_config: TestUserConfig = TestUserConfig()
    test_user_config.EMAIL = second_user_email
    test_user_config.USERNAME = second_user_username
    test_user_config.PASSWORD = await hash_password(test_user_config.PASSWORD)
    async with engine.begin() as conn:
        try:
            await conn.execute(insert(UserModel).values(**test_user_config.to_dict(to_lower=True)))
            await conn.commit()
        except IntegrityError:
            await conn.rollback()

    token_response: Response = await async_client.post(
        url=UsersRouterConfig.PREFIX + UsersURLPathsConfig.LOGIN,
        json={
            'username': second_user_username,
            'password': TestUserConfig.PASSWORD
        }
    )
    access_token: str = token_response.cookies[cookies_config.COOKIES_KEY]

    cookies: Cookies = Cookies()
    domain: str = os.environ.get('HOST', '0.0.0.0')
    cookies.set(name=cookies_config.COOKIES_KEY, value=access_token, domain=domain)

    delete_group_url_base: str = get_symbols_before_selected_symbol(
        symbol='{',
        string=URLPathsConfig.DELETE_GROUP
    )

    response: Response = await async_client.delete(
        url=RouterConfig.PREFIX + delete_group_url_base + '1',
        cookies=cookies
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_delete_group_fail_user_unauthorized(
        async_client: AsyncClient,
        create_test_group: None
) -> None:

    delete_group_url_base: str = get_symbols_before_selected_symbol(
        symbol='{',
        string=URLPathsConfig.DELETE_GROUP
    )

    response: Response = await async_client.delete(
        url=RouterConfig.PREFIX + delete_group_url_base + '1'
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
