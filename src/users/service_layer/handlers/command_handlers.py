from src.users.domain.events import UserRegisteredEvent
from src.users.interfaces.handlers import UsersCommandHandler
from src.users.domain.commands import (
    VerifyUserCredentialsCommand,
    RegisterUserCommand,
    VerifyUserEmailCommand,
    GetUserCommand
)
from src.users.domain.models import UserModel
from src.users.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    EmailIsNotVerifiedError,
    UserNotFoundError
)
from src.users.service_layer.service import UsersService
from src.users.utils import hash_password, verify_password


class RegisterUserCommandHandler(UsersCommandHandler):

    async def __call__(self, command: RegisterUserCommand) -> UserModel:
        """
        Registers a new user, if user with provided credentials doesn't exist, and creates event signaling that
        operation was successfully executed.
        """

        async with self._uow as uow:
            users_service: UsersService = UsersService(uow=self._uow)
            if await users_service.check_user_existence(email=command.email, username=command.username):
                raise UserAlreadyExistsError

            user: UserModel = UserModel(**await command.to_dict())
            user.password = await hash_password(user.password)

            user = await users_service.register_user(user=user)
            await user.protect_password()
            await uow.add_event(
                UserRegisteredEvent(
                    email=user.email,
                    username=user.username,
                    user_id=user.id
                )
            )

            return user


class VerifyUserCredentialsCommandHandler(UsersCommandHandler):

    async def __call__(self, command: VerifyUserCredentialsCommand) -> UserModel:
        """
        Checks, if provided by user credentials are valid.
        """

        users_service: UsersService = UsersService(uow=self._uow)

        user: UserModel
        if await users_service.check_user_existence(email=command.username):
            user = await users_service.get_user_by_email(email=command.username)
        elif await users_service.check_user_existence(username=command.username):
            user = await users_service.get_user_by_username(username=command.username)
        else:
            raise UserNotFoundError

        if not user.email_verified:
            raise EmailIsNotVerifiedError

        if not await verify_password(command.password, user.password):
            raise InvalidPasswordError

        await user.protect_password()
        return user


class VerifyUserEmailCommandHandler(UsersCommandHandler):

    async def __call__(self, command: VerifyUserEmailCommand) -> UserModel:
        """
        Confirms, that the provided by user email belongs to him.
        """

        users_service: UsersService = UsersService(uow=self._uow)
        user: UserModel = await users_service.verify_user_email(id=command.user_id)
        await user.protect_password()
        return user


class GetUserCommandHandler(UsersCommandHandler):

    async def __call__(self, command: GetUserCommand) -> UserModel:
        users_service: UsersService = UsersService(uow=self._uow)
        user: UserModel = await users_service.get_user_by_id(id=command.user_id)
        await user.protect_password()
        return user
