import re
from typing import Dict, Any, Optional

from src.core.scheme import HTMLContextScheme


def generate_html_context(**kwargs) -> Dict[str, Any]:
    """
    Dynamically creates HTML context for rendering HTML templates with provided arguments in Objects-Relating Style.
    """

    return HTMLContextScheme(**kwargs).model_dump()


def get_symbols_before_selected_symbol(string: str, symbol: str) -> str:
    """
    Iterates through provided string in try to return first match before provided symbol, using RegEx.
    If no provided symbol, returns the full string back.
    """

    result: Optional[re.Match] = re.match(
        pattern=rf'([^{symbol}]*){symbol}',  # all symbols before provided symbol
        string=string
    )

    if result:
        return result.group(1)  # 1 not to include provided symbol to the result

    return string
