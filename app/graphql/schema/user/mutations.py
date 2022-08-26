import strawberry

from app.graphql.schema.user.types import RegisterInput, RegisterOutput


@strawberry.type
class UserMutation:
    @strawberry.field
    async def register(self, input: RegisterInput) -> RegisterOutput:
        """
        register a new user
        """
        return RegisterOutput(token="")
