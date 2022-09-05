from typing import AsyncGenerator, Generator, Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users_tortoise import TortoiseUserDatabase

from app.core.config import settings
from app.db.models import User
from app.db.schema import UserCreateSchema
from app.internal import jwt_auth_backend
from app.utils.logger import app_logger


class UserDb(TortoiseUserDatabase[User, int]):
    def __init__(self, *args, **kwargs):
        super(UserDb, self).__init__(User, None)


async def get_user_db():
    """
    dependency for user_db
    """
    # yield UserDb()
    yield TortoiseUserDatabase(User)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

    async def validate_password(
        self, password: str, user: Union[UserCreateSchema, User]
    ) -> None:
        print(self.user_db.__dict__)
        if len(password) < 6:
            raise InvalidPasswordException(
                reason="Password should be at least 6 characters long."
            )

        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain user email."
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        app_logger.info("on after register")


# default user manager
user_manager = UserManager(user_db=TortoiseUserDatabase(User))


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    """
    user manager for dependency injection
    """
    yield UserManager(user_db=user_db)


# main component that ties together the various aspect of the authentication
fastapi_user = FastAPIUsers[User, int](
    get_user_manager=get_user_manager, auth_backends=[jwt_auth_backend]
)

# current user dependency to inject authenticated user into route
current_user = fastapi_user.current_user()
current_active_user = fastapi_user.current_user(active=True)
