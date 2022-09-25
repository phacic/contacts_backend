from enum import Enum
from typing import Union

from pydantic import BaseModel


class ErrorEnum(str, Enum):
    invalid_credentials = "INVALID_CREDENTIALS"
    inactive_user = "INACTIVE_USER"


class BaseError(BaseModel):
    text: Union[None, str]
    code: Union[None, ErrorEnum]
    description: Union[None, str]


class InvalidCredentialsError(BaseError):
    code = ErrorEnum.invalid_credentials
    text = "Invalid Credentials"
    description = "Provided credentials are not valid"


class InactiveUserError(BaseError):
    code = ErrorEnum.inactive_user
    text = "Inactive User"
    description = "User is deactivated"
