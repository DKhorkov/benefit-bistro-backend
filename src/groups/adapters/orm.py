from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapper
from datetime import datetime, timezone

from src.core.database.metadata import mapper_registry


group_members_table = Table(
    'group_members',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False, unique=True),
    Column(
        'group_id',
        Integer,
        ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True  # For updating members Set purpose
    ),
    Column(
        'user_id',
        Integer,
        ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    ),
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
    Column(
        'owner_id',
        Integer,
        ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    ),
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
    Map domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """

    # Imports here not to ruin alembic logics. Also, only for mappers they needed:
    from src.groups.domain.models import GroupModel, GroupMemberModel

    group_members_mapper: Mapper = mapper_registry.map_imperatively(
        class_=GroupMemberModel,
        local_table=group_members_table
    )

    mapper_registry.map_imperatively(
        class_=GroupModel,
        local_table=groups_table,
        properties={
            'members': relationship(
                group_members_mapper,
                backref='groups',
                collection_class=set,
                order_by=group_members_table.c.id,
                lazy='selectin'
            )
        }
    )
