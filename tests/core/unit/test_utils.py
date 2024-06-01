import pytest
from typing import Any, Dict

from src.core.utils import (
    generate_html_context,
    get_substring_before_selected_chars,
    get_substring_after_selected_chars
)


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


def test_get_substring_before_selected_chars_common_case() -> None:
    expected_result: str = 'someString'
    chars: str = '_'
    test_string: str = f'{expected_result}{chars}postfix'
    assert get_substring_before_selected_chars(string=test_string, chars=chars) == expected_result


def test_get_substring_before_selected_chars_without_selected_chars_in_string() -> None:
    chars: str = '_'
    test_string: str = 'Some text without selected symbol'
    assert get_substring_before_selected_chars(string=test_string, chars=chars) == test_string


def test_get_substring_after_selected_chars_common_case() -> None:
    expected_result: str = 'someString'
    chars: str = '_'
    test_string: str = f'prefix{chars}{expected_result}'
    assert get_substring_after_selected_chars(string=test_string, chars=chars) == expected_result


def test_get_substring_after_selected_chars_without_selected_chars_in_string() -> None:
    chars: str = '_'
    test_string: str = 'Some text without selected symbol'
    assert get_substring_after_selected_chars(string=test_string, chars=chars) == test_string
