from fastapi import status

from src.auth.constants import Error
from src.core.exceptions import DetailedHTTPException, PreconditionFailed, AlreadyExist, NotFound


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = Error.USER_NOT_AUTHENTICATED


class InvalidToken(PreconditionFailed):
    DETAIL = Error.INVALID_TOKEN


class InvalidPassword(PreconditionFailed):
    DETAIL = Error.INVALID_PASSWORD


class InvalidUser(PreconditionFailed):
    DETAIL = Error.INVALID_USER


class UserAlreadyExist(AlreadyExist):
    DETAIL = Error.USER_ALREADY_EXISTS


class UserNotFound(NotFound):
    DETAIL = Error.USER_NOT_FOUND
