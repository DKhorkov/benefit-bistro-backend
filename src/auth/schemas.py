from pydantic import BaseModel, EmailStr, field_validator

from src.auth.config import UserValidationConfig
from src.auth.constants import Error


class LoginUserScheme(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    @field_validator('password', mode='before')
    async def validate_password(cls, value: str) -> str:
        if not UserValidationConfig.PASSWORD_MIN_LENGTH <= len(value) <= UserValidationConfig.PASSWORD_MAX_LENGTH:
            raise ValueError(Error.PASSWORD_ERROR)

        return value


class RegisterUserScheme(LoginUserScheme):
    username: str

    @classmethod
    @field_validator('username', mode='before')
    async def validate_username(cls, value: str) -> str:
        if not UserValidationConfig.USERNAME_MIN_LENGTH <= len(value) <= UserValidationConfig.USERNAME_MAX_LENGTH:
            raise ValueError(Error.USERNAME_ERROR)

        return value
