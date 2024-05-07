from datetime import datetime, timezone
from fastapi import Depends
from jose import jwt, JWTError, ExpiredSignatureError

from src.auth.exceptions import InvalidTokenError, InvalidPasswordError, UserAlreadyExistError
from src.auth.models import UserModel, JWTDataModel
from src.auth.schemas import LoginUserScheme, RegisterUserScheme
from src.auth.utils import oauth2_scheme, create_access_token, verify_password
from src.auth.config import jwt_config
from src.auth.service import AuthService
from src.auth.units_of_work import SQLAlchemyUsersUnitOfWork


async def register_user(user_data: RegisterUserScheme) -> None:
    """
    Registers a new user, if user with provided credentials doesn't exist.
    """

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    if await auth_service.check_user_existence(email=user_data.email, username=user_data.username):
        raise UserAlreadyExistError

    await auth_service.register_user(user_data=user_data)


async def login_user(user_data: LoginUserScheme) -> str:
    """
    Logs in a user with provided credentials, if credentials are valid.
    """

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    user: UserModel = await auth_service.get_user_by_email(email=user_data.email)
    if not await verify_password(user_data.password, user.password):
        raise InvalidPasswordError

    jwt_data: JWTDataModel = JWTDataModel(user_id=user.id)
    return await create_access_token(jwt_data=jwt_data)


async def authenticate_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    """
    Authenticates user according to provided JWT token, if token is valid and hadn't expired.
    """

    try:
        payload = jwt.decode(token, jwt_config.ACCESS_TOKEN_SECRET_KEY, algorithms=[jwt_config.ACCESS_TOKEN_ALGORITHM])
        payload['exp'] = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)  # converting to datetime format
    except (JWTError, ExpiredSignatureError):
        raise InvalidTokenError

    jwt_data: JWTDataModel = JWTDataModel(**payload)
    if jwt_data.exp < datetime.now(tz=timezone.utc):
        raise InvalidTokenError

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    return await auth_service.authenticate_user(jwt_data=jwt_data)
