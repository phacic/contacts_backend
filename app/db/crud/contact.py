from typing import Any, Dict, List

from tortoise.models import in_transaction

from app.db.models import Address, Contact, Email, Phone, SignificantDate


async def create_new_contact(data: Dict) -> Contact:
    """
    save a new contact
    """
    phones = data.pop("phones", [])
    emails = data.pop("emails", [])
    dates = data.pop("significant_dates", [])

    # use transaction to save the pieces
    async with in_transaction():
        # create contact
        contact_obj = await Contact.create(**data)

        # the other pieces
        await create_phones(contact_obj, phones)
        await create_emails(contact_obj, emails)
        await create_sig_dates(contact_obj, dates)

        return await contact_obj


async def create_phones(c: Contact, phones_data: List[Dict]) -> Any:
    """ """
    if phones_data:
        phone_list = [Phone(contact=c, **p) for p in phones_data]
        return await Phone.bulk_create(phone_list)


async def create_emails(c: Contact, emails_data: List[Dict]) -> Any:
    """ """
    if emails_data:
        email_list = [Email(contact=c, **e) for e in emails_data]
        return await Email.bulk_create(email_list)


async def create_sig_dates(c: Contact, sig_data: List[Dict]) -> Any:
    """ """
    if sig_data:
        sig_list = [SignificantDate(contact=c, **s) for s in sig_data]
        return await SignificantDate.bulk_create(sig_list)


async def create_addresses(c: Contact, addresses_data: List[Dict]) -> Any:
    """"""
    if addresses_data:
        address_list = [Address(contact=c, **a) for a in addresses_data]
        return await Address.bulk_create(address_list)
