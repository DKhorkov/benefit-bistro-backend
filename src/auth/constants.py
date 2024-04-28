from src.core.constants import Error as BaseError


class Error(BaseError):
    USER_NOT_AUTHENTICATED: str = 'User not authenticated'
    PASSWORD_ERROR: str = 'Password must be between 8 and 20 characters'
    INVALID_TOKEN: str = 'Token has expired or is invalid'
