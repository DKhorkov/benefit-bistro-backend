from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from src.security.config import jwt_config
from src.core.interfaces import AbstractModel


@dataclass
class JWTDataModel(AbstractModel):
    user_id: int

    # Name should be only "exp" due to JWT docs. In other case will raise datetime encode error:
    exp: datetime = datetime.now(tz=timezone.utc) + timedelta(days=jwt_config.JWT_TOKEN_EXPIRE_DAYS)
