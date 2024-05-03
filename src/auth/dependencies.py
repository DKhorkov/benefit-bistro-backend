from datetime import datetime, timezone
from fastapi import Depends
from jose import jwt, JWTError

from src.auth.exceptions import InvalidToken, InvalidPassword, UserAlreadyExist
from src.auth.models import UserModel, JWTDataModel
from src.auth.schemas import LoginUserScheme, RegisterUserScheme
from src.auth.utils import oauth2_scheme, create_access_token, verify_password
from src.auth.config import jwt_config
from src.auth.service import AuthService


async def register_user(user_data: RegisterUserScheme) -> None:
    if await AuthService.check_user_existence(email=user_data.email):
        raise UserAlreadyExist

    await AuthService.register_user(user_data=user_data)


async def login_user(user_data: LoginUserScheme) -> str:
    user: UserModel = await AuthService.get_user_by_email(email=user_data.email)
    if not await verify_password(user_data.password, user.password):
        raise InvalidPassword

    jwt_data: JWTDataModel = JWTDataModel(user_id=user.id)
    return await create_access_token(jwt_data=jwt_data)


async def authenticate_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    try:
        payload = jwt.decode(token, jwt_config.ACCESS_TOKEN_SECRET_KEY, algorithms=[jwt_config.ACCESS_TOKEN_ALGORITHM])
    except JWTError:
        raise InvalidToken

    jwt_data: JWTDataModel = JWTDataModel(**payload)
    if jwt_data.expires < datetime.now(tz=timezone.utc):
        raise InvalidToken

    return await AuthService.authenticate_user(jwt_data=jwt_data)
