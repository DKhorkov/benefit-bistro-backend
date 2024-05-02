from fastapi import Depends
from jose import jwt, JWTError

from src.auth.exceptions import InvalidToken
from src.auth.models import UserModel
from src.auth.schemas import JWTDataScheme
from src.auth.utils import oauth2_scheme
from src.auth.config import jwt_config
from src.auth.service import AuthService


async def authenticate_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    try:
        payload = jwt.decode(token, jwt_config.ACCESS_TOKEN_SECRET_KEY, algorithms=[jwt_config.ACCESS_TOKEN_ALGORITHM])
    except JWTError:
        raise InvalidToken

    jwt_data: JWTDataScheme = JWTDataScheme(**payload)
    return await AuthService.authenticate_user(jwt_data=jwt_data)
