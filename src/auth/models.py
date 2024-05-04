from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from src.auth.config import jwt_config
from src.core.interfaces import BaseModel


@dataclass
class JWTDataModel(BaseModel):
    user_id: int

    # Name should be only "exp" due to JWT docs. In other case will raise datetime encode error:
    exp: datetime = datetime.now(tz=timezone.utc) + timedelta(minutes=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)


@dataclass
class UserModel(BaseModel):
    email: str
    password: str
    username: str

    # Optional args:
    id: int = 0
    email_confirmed: bool = False
