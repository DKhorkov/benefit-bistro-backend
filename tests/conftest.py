import pytest
import os
from httpx import AsyncClient, Cookies, Response
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.exc import ArgumentError, IntegrityError

from src.app import app
from src.auth.config import RouterConfig, URLPathsConfig, cookies_config
from src.auth.models import UserModel
from src.core.database.connection import DATABASE_URL
from src.core.database.orm import start_mappers, metadata
from src.auth.utils import hash_password
from tests.config import TestUserConfig
from tests.utils import get_base_url, drop_test_db


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Launch tests only on "asyncio" backend, without "trio" backend.
    """

    return 'asyncio'


@pytest.fixture(scope='session')
async def create_test_db() -> None:
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


@pytest.fixture(scope='session')
async def map_models_to_orm(create_test_db) -> None:
    """
    Create mappings from models to ORM according to DDD.
    """

    try:
        start_mappers()
    except ArgumentError:
        pass


@pytest.fixture(scope="session")
async def async_client(map_models_to_orm) -> AsyncClient:
    """
    Creates test app client for end-to-end tests to make requests to endpoints with.
    """

    async with AsyncClient(app=app, base_url=get_base_url()) as async_client:
        yield async_client

    drop_test_db()


@pytest.fixture
async def create_test_user_if_not_exists(map_models_to_orm) -> None:
    """
    Creates test user in test database, if user with provided credentials does not exist.
    """

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    test_user_config: TestUserConfig = TestUserConfig()
    test_user_config.PASSWORD = await hash_password(test_user_config.PASSWORD)
    async with engine.begin() as conn:
        try:
            await conn.execute(insert(UserModel).values(**test_user_config.to_dict(to_lower=True)))
            await conn.commit()
        except IntegrityError:
            await conn.rollback()


@pytest.fixture
async def access_token(async_client, create_test_user_if_not_exists) -> str:
    """
    Gets access token for test user, for usage during end-to-end tests to make request,
    which requires authenticated user.
    """

    response: Response = await async_client.post(
        url=RouterConfig.PREFIX + URLPathsConfig.LOGIN,
        json=TestUserConfig().to_dict(to_lower=True)
    )
    token: str = response.cookies[cookies_config.COOKIES_KEY]
    return token


@pytest.fixture
async def cookies(access_token) -> Cookies:
    """
    Creates cookies object for AsyncClient, for usage during end-to-end tests to make request,
    which requires authenticated user.
    """

    cookies: Cookies = Cookies()
    cookies.set(name=cookies_config.COOKIES_KEY, value=access_token, domain=os.environ.get("HOST"))
    return cookies
