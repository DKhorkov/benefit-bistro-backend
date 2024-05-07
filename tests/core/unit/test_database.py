import pytest
from typing import Sequence, Optional
from sqlalchemy import insert, select, CursorResult, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection

from src.auth.models import UserModel
from src.core.database.units_of_work import SQLAlchemyUnitOfWork
from tests.config import TestUserConfig


@pytest.mark.anyio
async def test_sqlalchemy_unit_of_work_saves_correct_model_and_commits(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()
    async with uow:
        new_user: UserModel = UserModel(**TestUserConfig().to_dict(to_lower=True))
        await uow._session.execute(insert(UserModel).values(**await new_user.to_dict()))
        await uow.commit()

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(email=TestUserConfig.EMAIL))
    result: Optional[Row] = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_unit_of_work_not_saves_incorrect_model_and_rollbacks(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    with pytest.raises(IntegrityError):
        uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()
        async with uow:
            await uow._session.execute(insert(UserModel))
            await uow.commit()

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(email=TestUserConfig.EMAIL))
    result: Sequence[Row] = cursor.all()
    assert not result
