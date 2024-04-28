from typing import Dict, Any

from src.core.scheme import ContextScheme


def generate_html_context(**kwargs) -> Dict[str, Any]:
    return ContextScheme(**kwargs).model_dump()
