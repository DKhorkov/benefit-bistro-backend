from fastapi import status

from src.auth.constants import Error
from src.core.exceptions import DetailedHTTPException


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = Error.USER_NOT_AUTHENTICATED


class InvalidToken(DetailedHTTPException):
    STATUS_CODE = status.HTTP_412_PRECONDITION_FAILED
    DETAIL = Error.INVALID_TOKEN
