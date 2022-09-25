from typing import Union

import strawberry

from app.graphql.schema.base import Error


@strawberry.input
class RegisterInput:
    fullname: str
    email: str
    password: str


@strawberry.type
class RegisterOutput:
    access_token: str
    error: Union[None, Error]


@strawberry.input
class LoginInput:
    username: str
    password: str


@strawberry.type
class LoginOutput:
    success: bool
    access_token: Union[None, str]
    token_type: Union[None, str]
    error: Union[None, Error]
