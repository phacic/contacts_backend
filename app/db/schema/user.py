from typing import Union
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi_users.schemas import BaseUser, BaseUserUpdate, BaseUserCreate
from pydantic import EmailStr

from app.db.models.user import User

UserSchema = pydantic_model_creator(User, name="User")

UserDefaultCreateSchema = pydantic_model_creator(User, name="UserCreate", exclude_readonly=True)


class UserCreateSchema(UserDefaultCreateSchema):
    email: EmailStr
    password: str


class UserUpdateSchema(UserDefaultCreateSchema):
    email: Union[None, EmailStr]
    password: Union[None, str]
    is_active: Union[None, bool]
    is_superuser: Union[None, bool]
    is_verified: Union[None, bool]

