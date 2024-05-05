from pydantic import BaseModel, EmailStr, field_validator

from src.auth.config import UserValidationConfig
from src.auth.exceptions import PasswordValidationError, UsernameValidationError


class LoginUserScheme(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password', mode='before')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not UserValidationConfig.PASSWORD_MIN_LENGTH <= len(value) <= UserValidationConfig.PASSWORD_MAX_LENGTH:
            raise PasswordValidationError

        return value


class RegisterUserScheme(LoginUserScheme):
    username: str

    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not UserValidationConfig.USERNAME_MIN_LENGTH <= len(value) <= UserValidationConfig.USERNAME_MAX_LENGTH:
            raise UsernameValidationError

        return value
