import pytest

from src.core.interfaces import BaseModel
from tests.core.fake_objects import TestModel


@pytest.mark.anyio
async def test_base_model_to_dict_basic() -> None:
    base_model: BaseModel = TestModel()
    assert await base_model.to_dict() == {'field1': 'test', 'field2': 123}


@pytest.mark.anyio
async def test_base_model_to_dict_with_exclude_existing_field() -> None:
    base_model: BaseModel = TestModel()
    assert await base_model.to_dict(exclude={'field1'}) == {'field2': 123}


@pytest.mark.anyio
async def test_base_model_to_dict_with_exclude_non_existing_field() -> None:
    base_model: BaseModel = TestModel()
    assert await base_model.to_dict(exclude={'some_non_existing_field'}) == {'field1': 'test', 'field2': 123}


@pytest.mark.anyio
async def test_base_model_to_dict_with_include() -> None:
    base_model: BaseModel = TestModel()
    assert await base_model.to_dict(include={'test': 123}) == {'field1': 'test', 'field2': 123, 'test': 123}
