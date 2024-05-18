from src.core.constants import ErrorDetails as BaseErrorDetails
from src.groups.config import GroupValidationConfig


class ErrorDetails(BaseErrorDetails):
    """
    Groups error messages for custom exceptions.
    """

    GROUP_ALREADY_EXISTS: str = 'Group with provided name already exists for current user.'
    GROUP_NAME_VALIDATION_ERROR: str = (f'Group name must be between {GroupValidationConfig.NAME_MIN_LENGTH} and '
                                        f'{GroupValidationConfig.NAME_MAX_LENGTH} characters inclusive')
    GROUP_NOT_FOUND: str = 'Group not found.'
    GROUP_OWNER_ERROR: str = 'Group doe not belong to current user.'
