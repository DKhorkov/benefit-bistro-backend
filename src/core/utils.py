import re
from typing import Dict, Any, Optional

from src.core.scheme import HTMLContextScheme


def generate_html_context(**kwargs) -> Dict[str, Any]:
    """
    Dynamically creates HTML context for rendering HTML templates with provided arguments in Objects-Relating Style.
    """

    return HTMLContextScheme(**kwargs).model_dump()


def get_substring_before_chars(string: str, chars: str) -> str:
    """
    Iterates through provided string and trys to return first match before provided chars, using RegEx.
    If no provided chars in string, returns the full string back.
    """

    result: Optional[re.Match] = re.match(
        pattern=rf'([^{chars}]*){chars}',  # all chars before provided chars
        string=string
    )

    if result:
        return result.group(1)  # 1 not to include provided chars to the result

    return string


def get_substring_after_chars(string: str, chars: str) -> str:
    """
    Iterates through provided string and trys to return first match after provided chars, using RegEx.
    If no provided chars in string, returns the full string back.
    """

    result: Optional[re.Match] = re.search(
        pattern=rf'(?<={chars})[^.]*',  # all chars after provided chars
        string=string
    )

    if result:
        return result.group()

    return string
