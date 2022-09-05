from typing import List, Union

import strawberry


@strawberry.type
class PhoneType:
    phone_number: str


@strawberry.type
class ContactType:
    id: int
    user_id: Union[None, int]
    phones: Union[None, List[PhoneType]]
