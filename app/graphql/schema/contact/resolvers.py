from typing import List, Optional, Any

from strawberry.types import Info

from app.db.crud import get_user_contacts
from app.graphql.schema.contact.types import ContactType


async def get_contacts(
    user_id: Optional[int] = None, root: Optional[Any] = None, info: Optional[Info] = None,
) -> List[ContactType]:
    cs = await get_user_contacts(user_id=user_id)
    return [ContactType(id=c.id, user_id=c.user_id, phones=c.phones) for c in cs]
