import pytest
from anyio.from_thread import BlockingPortal

from app.db.models import Contact, Phone, User
from tests.factory import (
    AddressFactory,
    ContactFactory,
    EmailFactory,
    PhoneFactory,
    SignificantDateFactory,
    SocialMediaFactory,
    UserFactory,
)


def test_create_user(app_portal: BlockingPortal) -> None:
    """"""
    user = app_portal.call(UserFactory)

    async def get_user_count():
        return await User.all().count()

    db_count = app_portal.call(get_user_count)

    assert user is not None
    assert db_count == 1


def test_create_contact(app_portal: BlockingPortal) -> None:
    """ """
    contacts = app_portal.call(ContactFactory.create_batch, *(2,))

    async def get_contacts_count():
        return await Contact.all().count()

    db_count = app_portal.call(get_contacts_count)
    assert db_count == 2

    for c in contacts:
        assert c.user_id is not None


@pytest.mark.anyio
async def test_contact_with_details(app_portal: BlockingPortal) -> None:
    """"""

    contact = app_portal.call(ContactFactory.call_create)
    assign_contact = {"contact": contact}

    phones = app_portal.call(PhoneFactory.call_create_batch, *(2, assign_contact))
    emails = app_portal.call(EmailFactory.call_create_batch, *(2, assign_contact))
    address = app_portal.call(AddressFactory.call_create, *(assign_contact,))
    dates = app_portal.call(SignificantDateFactory.call_create, *(assign_contact,))
    socials = app_portal.call(
        SocialMediaFactory.call_create_batch, *(3, assign_contact)
    )

    # async def count_contacts():
    #     return await Contact.all().count()

    async def count_phones():
        return await Phone.all().count()

    # contact_count = app_portal.call(count_contacts)
    phones_count = app_portal.call(count_phones)

    # assert contact_count == 1
    assert phones_count == 2

    # phone should be related to contact
    for p in phones:
        assert p.contact.id == contact.id

    # emails should be related to contact
    for e in emails:
        assert e.contact.id == contact.id

    assert address.contact_id == contact.id
    assert dates.contact_id == contact.id

    for s in socials:
        assert s.contact_id == contact.id
