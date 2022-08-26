from typing import List, Union
import strawberry
from strawberry.types import Info

from app.graphql.schema.contact.types import ContactType
from app.graphql.schema.contact.resolvers import get_contacts


@strawberry.type
class ContactQuery:
    @strawberry.field
    async def contacts(self, root, info: Info) -> Union[None, List[ContactType]]:
        return await get_contacts(root=root, info=info)
    # contacts: Union[None, List[ContactType]] = strawberry.field(resolver=get_contacts(1))

