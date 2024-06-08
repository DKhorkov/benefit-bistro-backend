from typing import List
from pydantic import BaseModel, field_validator, EmailStr

from src.groups.config import GroupValidationConfig
from src.groups.exceptions import GroupNameValidationError


class CreateOrUpdateGroupScheme(BaseModel):
    name: str

    @field_validator('name', mode='before')
    @classmethod
    def validate_group_name(cls, value: str) -> str:
        if not GroupValidationConfig.NAME_MIN_LENGTH <= len(value) <= GroupValidationConfig.NAME_MAX_LENGTH:
            raise GroupNameValidationError

        return value


class UpdateGroupMembersScheme(BaseModel):
    group_members_ids: List[int] = []


class InviteGroupMembersScheme(BaseModel):
    emails: List[EmailStr] = []
    
