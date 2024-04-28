from src.core.constants import Error as BaseError
from src.auth.config import PasswordConfig


class Error(BaseError):
    USER_NOT_AUTHENTICATED: str = 'User not authenticated'
    PASSWORD_ERROR: str = (f'Password must be between {PasswordConfig.MIN_LENGTH} and '
                           f'{PasswordConfig.MAX_LENGTH} characters inclusive.')
    INVALID_TOKEN: str = 'Token has expired or is invalid'
