from typing import Union
from datetime import datetime

from fastapi_users import schemas
from pydantic import EmailStr


class UserSchema(schemas.BaseUser):
    status: str
    date_joined: datetime
    updated_at: datetime


class UserCreateSchema(schemas.BaseUserCreate):
    email: EmailStr
    password: str


class UserUpdateSchema(schemas.BaseUserUpdate):
    email: Union[None, EmailStr]
    password: Union[None, str]
    is_active: Union[None, bool]
    is_superuser: Union[None, bool]
    is_verified: Union[None, bool]
