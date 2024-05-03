from src.core.constants import Error as BaseError
from src.auth.config import UserValidationConfig


class Error(BaseError):
    USER_NOT_AUTHENTICATED: str = 'User not authenticated'
    PASSWORD_ERROR: str = (f'Password must be between {UserValidationConfig.PASSWORD_MIN_LENGTH} and '
                           f'{UserValidationConfig.PASSWORD_MAX_LENGTH} characters inclusive')
    USERNAME_ERROR: str = (f'Username must be between {UserValidationConfig.USERNAME_MIN_LENGTH} and '
                           f'{UserValidationConfig.USERNAME_MAX_LENGTH} characters inclusive')
    INVALID_TOKEN: str = 'Token has expired or is invalid'
    INVALID_PASSWORD: str = 'Provided password is invalid'
    INVALID_USER: str = 'Current user is invalid'
    USER_ALREADY_EXISTS: str = 'User with provided credentials already exists'
    USER_NOT_FOUND: str = 'User with provided credentials not found'
