from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise

from app.api import v1_router as api_v1_router
from app.api.deps import fastapi_user
from app.core.config import settings
from app.core.tortoise import orm_config
from app.db.schema import UserCreateSchema, UserSchema
from app.graphql import v1_router as graphql_v1_router
from app.internal import jwt_auth_backend
from app.utils.logger import app_logger

app = FastAPI(
    title="Contacts App",
    description="A contacts app with both REST and GraphQL endpoints.",
)

# routers
app.include_router(
    router=fastapi_user.get_auth_router(jwt_auth_backend),
    tags=["auth-jwt"],
    prefix="/auth",
)
app.include_router(
    router=fastapi_user.get_register_router(
        user_schema=UserSchema, user_create_schema=UserCreateSchema
    ),
    tags=["auth-jwt"],
    prefix="/auth",
)
app.include_router(router=api_v1_router, prefix=settings.API, tags=[f"{settings.API}"])
app.include_router(
    router=graphql_v1_router, prefix=settings.GRAPH_QL, tags=[f"{settings.GRAPH_QL}"]
)

# middleware
origins = [
    # "localhost",
    # "localhost:7770",
    # "http://localhost",
    # "http://localhost:7770",
    # "http://testserver"
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=origins,
)

# register tortoise orm
app_logger.debug("registering tortoise-orm")
register_tortoise(app=app, config=orm_config, add_exception_handlers=True)


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    app_logger.info("redirecting to /docs")
    return RedirectResponse(url="/docs")
