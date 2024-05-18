from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import registry
from datetime import datetime, timezone

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

users_table = Table(
    'users',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
    Column('email', String(50), nullable=False, unique=True),
    Column('password', String(100), nullable=False),
    Column('username', String(20), nullable=False, unique=True),
    Column('email_verified', Boolean(), nullable=False, default=False),
    Column('created_at', DateTime(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc)),
    Column(
        'updated_at',
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc)
    )
)

groups_table = Table(
    'groups',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
    Column('owner_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column('name', String(50), nullable=False, unique=False),
    Column('created_at', DateTime(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc)),
    Column(
        'updated_at',
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc)
    )
)


def start_mappers():
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """

    # Imports here not to ruin alembic logics. Also, only for mappers they needed:
    from src.auth.models import UserModel
    from src.groups.models import GroupModel

    mapper_registry.map_imperatively(class_=UserModel, local_table=users_table)
    mapper_registry.map_imperatively(class_=GroupModel, local_table=groups_table)
