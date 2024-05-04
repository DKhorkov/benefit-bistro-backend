from typing import Dict, Any

from src.core.scheme import HTMLContextScheme


def generate_html_context(**kwargs) -> Dict[str, Any]:
    """
    Dynamically creates HTML context for rendering HTML templates with provided arguments in Objects-Relating Style.
    """

    return HTMLContextScheme(**kwargs).model_dump()
