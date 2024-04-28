from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, PositiveInt, EmailStr, field_validator

from src.auth.config import PasswordConfig, jwt_config
from src.auth.constants import Error


class JWTDataScheme(BaseModel):
    user_id: PositiveInt
    expires: datetime = datetime.now(timezone.utc) + timedelta(minutes=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)


class AuthUserScheme(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    @field_validator('password', mode='before')
    async def validate_username(cls, value: str) -> str:
        if not PasswordConfig.MIN_LENGTH <= len(value) <= PasswordConfig.MAX_LENGTH:
            raise ValueError(Error.PASSWORD_ERROR)

        return value
