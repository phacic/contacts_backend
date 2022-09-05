import strawberry
from fastapi import Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi_users.authentication.transport.bearer import BearerResponse
from strawberry.types import Info

from app.api.deps import user_manager
from app.graphql.schema.base import Error
from app.graphql.schema.user.types import (
    LoginInput,
    LoginOutput,
    RegisterInput,
    RegisterOutput,
)
from app.internal import get_jwt_strategy, jwt_auth_backend


@strawberry.type
class UserMutation:
    @strawberry.field
    async def register(self, input_data: RegisterInput) -> RegisterOutput:
        """
        register a new user
        """
        return RegisterOutput(token="")

    @strawberry.field
    async def login(self, info: Info, input_data: LoginInput) -> LoginOutput:
        """
        log in for an existing user
        """
        form = OAuth2PasswordRequestForm(
            username=input_data.username, password=input_data.password, scope=""
        )
        user = await user_manager.authenticate(credentials=form)

        if user is None or not user.is_active:
            err = Error(err_text="bad credentials", code=0, description="")
            return LoginOutput(
                success=False, access_token=None, token_type=None, error=err
            )

        strategy = get_jwt_strategy()
        resp = Response()
        bearer_resp: BearerResponse = await jwt_auth_backend.login(
            user=user, strategy=strategy, response=resp
        )

        return LoginOutput(
            success=True,
            access_token=bearer_resp.access_token,
            token_type=bearer_resp.token_type,
            error=None,
        )
