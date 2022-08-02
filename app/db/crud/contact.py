from typing import Dict, Optional, Any, List
from tortoise.models import in_transaction

from app.db.models import (
    Contact, Phone, Email, SignificantDate, Address
)
from app.db.schema import (
    ContactCreateSchema, ContactSchema, PhoneSchema, PhoneCreateSchema
)


async def create_contact(data: ContactCreateSchema) -> ContactSchema:
    """
    save a new contact
    """
    data_dict = data.dict(exclude_unset=True)
    phones = data_dict.pop("phones", [])
    emails = data_dict.pop("emails", [])
    dates = data_dict.pop("significant_dates", [])

    # use transaction to save the pieces
    async with in_transaction():
        # create contact
        contact_obj = await Contact.create(**data_dict)

        # the other pieces
        await create_phones(phones)
        await create_emails(emails)
        await create_sig_dates(dates)

        return ContactSchema.from_tortoise_orm(contact_obj)


async def create_phones(phones_data: List[Dict]) -> Any:
    """ """
    phone_list = [Phone(**p) for p in phones_data]
    return await Phone.bulk_create(phone_list)


async def create_emails(emails_data: List[Dict]) -> Any:
    """ """
    email_list = [Email(**e) for e in emails_data]
    return await Email.bulk_create(email_list)


async def create_sig_dates(sig_data: List[Dict]) -> Any:
    """ """
    sig_list = [SignificantDate(**s) for s in sig_data]
    return await SignificantDate.bulk_create(sig_list)


async def create_addresses(addresses_data: List[Dict]) -> Any:
    """"""
    address_list = [Address(**a) for a in addresses_data]
    return await Address.bulk_create(address_list)
