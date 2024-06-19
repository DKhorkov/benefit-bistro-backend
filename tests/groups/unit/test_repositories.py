import pytest
from typing import Optional, List, Sequence
from sqlalchemy import select, CursorResult, Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker

from src.groups.domain.models import GroupModel
from src.groups.adapters.repositories import SQLAlchemyGroupsRepository
from tests.config import FakeGroupConfig


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_get_success(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    group: Optional[GroupModel] = await SQLAlchemyGroupsRepository(session=session).get(id=1)

    assert group is not None
    assert group.id == 1
    assert group.name == FakeGroupConfig.NAME
    assert group.owner_id == FakeGroupConfig.OWNER_ID


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_get_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    group: Optional[GroupModel] = await SQLAlchemyGroupsRepository(session=session).get(id=1)
    assert group is None


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_get_by_owner_and_name_success(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    group: Optional[GroupModel] = await SQLAlchemyGroupsRepository(session=session).get_by_owner_and_name(
        owner_id=FakeGroupConfig.OWNER_ID,
        name=FakeGroupConfig.NAME
    )

    assert group is not None
    assert group.name == FakeGroupConfig.NAME
    assert group.owner_id == FakeGroupConfig.OWNER_ID


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_get_by_owner_and_name_fail_by_owner_id(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    group: Optional[GroupModel] = await SQLAlchemyGroupsRepository(session=session).get_by_owner_and_name(
        owner_id=2,
        name=FakeGroupConfig.NAME
    )

    assert group is None


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_get_by_owner_and_name_fail_by_name(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    group: Optional[GroupModel] = await SQLAlchemyGroupsRepository(session=session).get_by_owner_and_name(
        owner_id=FakeGroupConfig.OWNER_ID,
        name='someGroupName'
    )

    assert group is None


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_get_user_groups(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_groups: List[GroupModel] = await SQLAlchemyGroupsRepository(session=session).get_user_groups(
        user_id=FakeGroupConfig.OWNER_ID
    )
    assert len(user_groups) == 1
    group: GroupModel = user_groups[0]
    assert group.id == 1
    assert group.owner_id == FakeGroupConfig.OWNER_ID
    assert group.name == FakeGroupConfig.NAME


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_get_empty_user_groups(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user_groups: List[GroupModel] = await SQLAlchemyGroupsRepository(session=session).get_user_groups(
        user_id=FakeGroupConfig.OWNER_ID
    )
    assert len(user_groups) == 0


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_list(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    groups_list: List[GroupModel] = await SQLAlchemyGroupsRepository(session=session).list()
    assert len(groups_list) == 1
    group: GroupModel = groups_list[0]
    assert group.id == 1
    assert group.owner_id == FakeGroupConfig.OWNER_ID
    assert group.name == FakeGroupConfig.NAME


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_empty_list(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    groups_list: List[GroupModel] = await SQLAlchemyGroupsRepository(session=session).list()
    assert len(groups_list) == 0


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_delete_existing_group(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(GroupModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 1

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyGroupsRepository(session=session).delete(id=1)

    cursor = await async_connection.execute(select(GroupModel))
    result = cursor.all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_delete_non_existing_group(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(GroupModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 0

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyGroupsRepository(session=session).delete(id=1)


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_add_group_success(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(
        select(GroupModel).filter_by(
            name=FakeGroupConfig.NAME,
            owner_id=FakeGroupConfig.OWNER_ID
        )
    )
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    group: GroupModel = GroupModel(**FakeGroupConfig().to_dict(to_lower=True))
    await SQLAlchemyGroupsRepository(session=session).add(model=group)

    cursor = await async_connection.execute(
        select(GroupModel).filter_by(
            name=FakeGroupConfig.NAME,
            owner_id=FakeGroupConfig.OWNER_ID
        )
    )
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_add_group_success_with_provided_already_existing_id(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(GroupModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    group_name: str = 'someGroupName'
    group: GroupModel = GroupModel(**FakeGroupConfig().to_dict(to_lower=True))
    group.name = group_name
    group.id = 1

    await SQLAlchemyGroupsRepository(session=session).add(model=group)

    cursor = await async_connection.execute(
        select(GroupModel).filter_by(
            name=group_name,
            owner_id=FakeGroupConfig.OWNER_ID
        )
    )
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_update_existing_group(
        create_test_group: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(GroupModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    group_name: str = 'someGroupName'
    group: GroupModel = GroupModel(**FakeGroupConfig().to_dict(to_lower=True))
    group.name = group_name

    await SQLAlchemyGroupsRepository(session=session).update(id=1, model=group)

    cursor = await async_connection.execute(select(GroupModel).filter_by(name=group_name))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_groups_repository_update_non_existing_group(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(GroupModel).filter_by(id=1))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    group: GroupModel = GroupModel(**FakeGroupConfig().to_dict(to_lower=True))
    with pytest.raises(NoResultFound):
        await SQLAlchemyGroupsRepository(session=session).update(id=1, model=group)
