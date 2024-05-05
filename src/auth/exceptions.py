from fastapi import status

from src.auth.constants import ErrorDetails
from src.core.exceptions import (
    DetailedHTTPException,
    PreconditionFailedError,
    AlreadyExistError,
    NotFoundError,
    ValidationError
)


class NotAuthenticatedError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = ErrorDetails.USER_NOT_AUTHENTICATED


class InvalidTokenError(PreconditionFailedError):
    DETAIL = ErrorDetails.INVALID_TOKEN


class InvalidPasswordError(PreconditionFailedError):
    DETAIL = ErrorDetails.INVALID_PASSWORD


class InvalidUserError(PreconditionFailedError):
    DETAIL = ErrorDetails.INVALID_USER


class UserAlreadyExistError(AlreadyExistError):
    DETAIL = ErrorDetails.USER_ALREADY_EXISTS


class UserNotFoundError(NotFoundError):
    DETAIL = ErrorDetails.USER_NOT_FOUND


class UsernameValidationError(ValidationError):
    DETAIL = ErrorDetails.USERNAME_VALIDATION_ERROR


class PasswordValidationError(ValidationError):
    DETAIL = ErrorDetails.PASSWORD_VALIDATION_ERROR
