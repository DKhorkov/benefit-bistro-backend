from dataclasses import dataclass

from src.core.interfaces import BaseModel


@dataclass
class TestModel(BaseModel):
    """
    Inherited model from base just to test BaseModel's methods.
    """

    field1: str = 'test'
    field2: int = 123
