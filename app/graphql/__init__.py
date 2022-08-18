from fastapi import APIRouter
from strawberry import Schema
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import Query

v1_router = APIRouter()
# graphql router
graphql_schema = Schema(query=Query)
v1_router.include_router(
    router=GraphQLRouter(schema=graphql_schema, graphiql=True, debug=True),
    prefix="/v1",
)