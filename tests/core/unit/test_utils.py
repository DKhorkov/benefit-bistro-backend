import pytest
from typing import Any, Dict

from src.core.utils import generate_html_context


def test_generate_html_context_success() -> None:
    kwargs: Dict[str, Any] = {'title': 'Some title'}
    assert generate_html_context(**kwargs) == {'title': 'Some title'}


def test_generate_html_context_success_with_extra_args() -> None:
    kwargs: Dict[str, Any] = {'title': 'Some title', 'non_existing_arg': 22}
    assert generate_html_context(**kwargs) == {'title': 'Some title'}


def test_generate_html_context_fail() -> None:
    with pytest.raises(ValueError) as exc_info:
        kwargs: Dict[str, Any] = {'non_existing_arg': 22}
        generate_html_context(**kwargs)

    assert 'validation error for HTMLContextScheme\ntitle' in str(exc_info.value)
