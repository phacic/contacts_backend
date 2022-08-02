from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from tortoise.contrib.fastapi import register_tortoise
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from app.core.tortoise import orm_config
from app.utils.logger import app_logger
from app.graphql.schema import Query
from app.api import (contact_router)

app = FastAPI(title="Contacts App", description="A contacts app with both REST and GraphQL endpoints.")

# routers
# strawberry graphql router
graphql_schema = Schema(query=Query)
app.include_router(router=GraphQLRouter(schema=graphql_schema, graphiql=True, debug=True), prefix="/graphql")

# app routers
app.include_router(router=contact_router, prefix="/contact")

# middleware
origins = [
    "localhost",
    "localhost:7770",
    "http://localhost",
    "http://localhost:7770",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=origins,
)

# register tortoise orm
app_logger.debug("registering tortoise-orm")
register_tortoise(
    app=app, config=orm_config, add_exception_handlers=True
)
