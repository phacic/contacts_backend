from typing import Any, Dict, List, Optional

from tortoise.models import in_transaction

from app.db.models import Address, Contact, Email, Phone, SignificantDate, SocialMedia
from app.db.models.constant import StatusOptions
from app.db.schema import ContactSchema


async def create_new_contact(data: Dict) -> Contact:
    """
    save a new contact
    """
    phones = data.pop("phones", [])
    emails = data.pop("emails", [])
    dates = data.pop("significant_dates", [])
    addresses = data.pop("addresses", [])
    socials = data.pop("socials", [])

    # use transaction to save the pieces
    async with in_transaction():
        # create contact
        contact_obj = await Contact.create(**data)

        # the other pieces
        await create_phones(contact_obj, phones)
        await create_emails(contact_obj, emails)
        await create_sig_dates(contact_obj, dates)
        await create_addresses(contact_obj, addresses)
        await create_socials(contact_obj, socials)

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


async def create_socials(c: Contact, social_data: List[Dict]) -> Any:
    """"""
    if social_data:
        social_list = [SocialMedia(contact=c, **s) for s in social_data]
        return await SocialMedia.bulk_create(social_list)


async def get_user_contact(user_id: int, contact_id: int) -> Optional[Contact]:
    """
    get a contact created by a user
    """
    qs = Contact.filter(id=contact_id, user_id=user_id).first()
    return await ContactSchema.from_queryset_single(qs)


async def get_user_contacts(user_id: Optional[int] = None) -> List[Contact]:
    """
    contacts created by a user
    """
    qs = (
        Contact.active_objects()
        .filter(user_id=user_id)
        .prefetch_related(
            "phones", "emails", "significant_dates", "addresses", "socials"
        )
    )
    return await ContactSchema.from_queryset(qs)


async def deactivate_contact(user_id: int, contact_id: int) -> None:
    """
    set a contact status to inactive
    """
    await Contact.active_objects().filter(user_id=user_id, id=contact_id).update(
        status=StatusOptions.Inactive.value
    )
