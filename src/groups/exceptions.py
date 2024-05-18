from src.groups.constants import ErrorDetails
from src.core.exceptions import (
    AlreadyExistsError,
    ValidationError,
    NotFoundError,
    PermissionDeniedError
)


class GroupAlreadyExistsError(AlreadyExistsError):
    DETAIL = ErrorDetails.GROUP_ALREADY_EXISTS


class GroupNameValidationError(ValidationError):
    DETAIL = ErrorDetails.GROUP_NAME_VALIDATION_ERROR


class GroupNotFoundError(NotFoundError):
    DETAIL = ErrorDetails.GROUP_NOT_FOUND


class GroupOwnerError(PermissionDeniedError):
    DETAIL = ErrorDetails.GROUP_OWNER_ERROR
