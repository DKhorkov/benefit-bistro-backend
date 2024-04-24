from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Paths:
    TEMPLATES: Path = Path("./templates")
    STATIC: Path = Path("./static")
