from typing import Union

import strawberry
from strawberry.tools import merge_types

from app.graphql.schema.contact import ContactQuery
from app.graphql.schema.user import UserMutation

__all__ = ["Query", "Mutations"]


Query = merge_types("Query", (ContactQuery,))
Mutations = merge_types("Mutations", (UserMutation,))
# Subscriptions = merge_types("Subscriptions", ())
