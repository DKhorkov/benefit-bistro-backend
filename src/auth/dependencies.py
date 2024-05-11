from fastapi import Depends

from src.auth.exceptions import InvalidPasswordError, UserAlreadyExistError
from src.auth.models import UserModel
from src.security.models import JWTDataModel
from src.auth.schemas import LoginUserScheme, RegisterUserScheme
from src.auth.utils import oauth2_scheme, verify_password
from src.auth.service import AuthService
from src.auth.units_of_work import SQLAlchemyUsersUnitOfWork
from src.security.utils import parse_jwt_token


async def register_user(user_data: RegisterUserScheme) -> UserModel:
    """
    Registers a new user, if user with provided credentials doesn't exist.
    """

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    if await auth_service.check_user_existence(email=user_data.email, username=user_data.username):
        raise UserAlreadyExistError

    return await auth_service.register_user(user_data=user_data)


async def login_user(user_data: LoginUserScheme) -> UserModel:
    """
    Logs in a user with provided credentials, if credentials are valid.
    """

    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    user: UserModel = await auth_service.get_user_by_email(email=user_data.email)
    if not await verify_password(user_data.password, user.password):
        raise InvalidPasswordError

    return user


async def authenticate_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    """
    Authenticates user according to provided JWT token, if token is valid and hadn't expired.
    """

    jwt_data: JWTDataModel = await parse_jwt_token(token=token)
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    return await auth_service.authenticate_user(jwt_data=jwt_data)


async def verify_user_email(token: str) -> UserModel:
    """
    Confirms, that the provided by user email belongs to him according provided JWT token.
    """

    jwt_data: JWTDataModel = await parse_jwt_token(token=token)
    auth_service: AuthService = AuthService(uow=SQLAlchemyUsersUnitOfWork())
    return await auth_service.verify_user_email(jwt_data=jwt_data)
