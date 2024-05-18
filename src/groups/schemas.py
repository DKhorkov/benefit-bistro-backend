from typing import Optional
from pydantic import BaseModel, field_validator

from src.groups.config import GroupValidationConfig
from src.groups.exceptions import GroupNameValidationError


class CreateGroupScheme(BaseModel):
    name: str
    owner_id: Optional[int] = None

    @field_validator('name', mode='before')
    @classmethod
    def validate_group_name(cls, value: str) -> str:
        if not GroupValidationConfig.NAME_MIN_LENGTH <= len(value) <= GroupValidationConfig.NAME_MAX_LENGTH:
            raise GroupNameValidationError

        return value
