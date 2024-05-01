from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.core.database.config import database_config


DATABASE_URL: str = 'postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
    database_config.DATABASE_USER,
    database_config.DATABASE_PASSWORD,
    database_config.DATABASE_HOST,
    database_config.DATABASE_PORT,
    database_config.DATABASE_NAME
)

engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL,
    pool_pre_ping=database_config.DATABASE_POOL_PRE_PING,
    pool_recycle=database_config.DATABASE_POOL_RECYCLE,
    echo=database_config.DATABASE_ECHO
)
