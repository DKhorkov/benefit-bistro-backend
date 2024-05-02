from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, MetaData
from sqlalchemy.orm import registry
from datetime import datetime, timezone

from src.auth.models import UserModel


metadata = MetaData()
mapper_registry = registry(metadata=metadata)


users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("email", String(50), nullable=False),
    Column("password", String(100), nullable=False),
    Column("username", String(20), nullable=False),
    Column("email_confirmed", Boolean(), nullable=False, default=False),
    Column("created_at", DateTime(timezone=False), nullable=False, default=datetime.now(tz=timezone.utc)),
    Column("updated_at", DateTime(timezone=False), nullable=False, onupdate=datetime.now(tz=timezone.utc)),
)

mapper_registry.map_imperatively(class_=UserModel, local_table=users_table)
