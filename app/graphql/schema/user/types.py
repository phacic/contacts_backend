import strawberry


@strawberry.input
class RegisterInput:
    fullname: str
    email: str
    password: str


@strawberry.type
class RegisterOutput:
    token: str
