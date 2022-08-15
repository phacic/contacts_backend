from typing import List

import strawberry

from app.graphql.resolvers import get_contacts


@strawberry.type
class Query:
    contacts: List = strawberry.field(resolver=get_contacts)
