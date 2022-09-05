from datetime import datetime
from typing import Union

from fastapi_users import schemas
from pydantic import EmailStr


class UserSchema(schemas.BaseUser):
    status: str
    date_joined: datetime
    updated_at: datetime


class UserCreateSchema(schemas.CreateUpdateDictModel):
    """
    Schema for registering a member. Did not inherit from schemas. BaseUserCreate
    because we do not want to include the following in the schema
        is_active: Optional[bool]
        is_superuser: Optional[bool]
        is_verified: Optional[bool]
    """

    full_name: str
    email: EmailStr
    password: str


class UserUpdateSchema(schemas.BaseUserUpdate):
    email: Union[None, EmailStr]
    password: Union[None, str]
    is_active: Union[None, bool]
    is_superuser: Union[None, bool]
    is_verified: Union[None, bool]
