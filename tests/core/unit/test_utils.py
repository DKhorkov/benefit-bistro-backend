import pytest
from typing import Any, Dict

from src.core.utils import generate_html_context, get_symbols_before_selected_symbol


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


def test_get_symbols_before_selected_symbol_common_case() -> None:
    expected_result: str = 'someString'
    symbol: str = '_'
    test_string: str = f'{expected_result}{symbol}postfix'
    assert get_symbols_before_selected_symbol(string=test_string, symbol=symbol) == expected_result


def test_get_symbols_before_selected_symbol_without_selected_symbol_in_string() -> None:
    symbol: str = '_'
    test_string: str = 'Some text without selected symbol'
    assert get_symbols_before_selected_symbol(string=test_string, symbol=symbol) == test_string
