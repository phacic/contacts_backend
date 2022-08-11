from typing import Union, Optional
from fastapi import Depends, Request
from fastapi_users_tortoise import TortoiseUserDatabase
from fastapi_users import BaseUserManager, IntegerIDMixin, InvalidPasswordException

from app.core.config import settings
from app.db.models import User
from app.db.schema import UserCreateSchema
from app.utils.logger import app_logger


async def get_user_db():
    """
    dependency for user_db
    """
    yield TortoiseUserDatabase[User, int]


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

    async def validate_password(
            self, password: str, user: Union[UserCreateSchema, User]
    ) -> None:
        if len(password) < 6:
            raise InvalidPasswordException(reason="Password should be at least 6 characters long.")

        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain user email.")

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ) -> None:
        app_logger.info("on after register")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db=user_db)
