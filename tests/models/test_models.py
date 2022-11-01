import pytest
from fastapi.testclient import TestClient
from asyncio import run, Future

from app.db.models import Contact, Phone, User
from tests.factory import (
    AddressFactory,
    ContactFactory,
    EmailFactory,
    PhoneFactory,
    SignificantDateFactory,
    SocialMediaFactory,
    UserFactory
)


def test_create_user(app_client) -> None:
    """"""
    user = app_client.portal.call(UserFactory)

    async def get_user_count():
        return await User.all().count()

    db_count = app_client.portal.call(get_user_count)

    assert user is not None
    assert db_count == 1


def test_create_contact(app_client) -> None:
    """ """
    contacts = app_client.portal.call(ContactFactory.create_batch, *(2,))

    async def get_contacts_count():
        return await Contact.all().count()

    db_count = app_client.portal.call(get_contacts_count)
    assert db_count == 2

    for c in contacts:
        assert c.user_id is not None


@pytest.mark.anyio
async def test_contact_with_details(app_client) -> None:
    """"""
    contact = app_client.portal.call(ContactFactory)
    f: Future = Future()
    app_client.portal._spawn_task_from_thread(PhoneFactory.create_batch, (2,), {}, None, f)
    phones = f.result()
    emails = EmailFactory.create_batch(2, contact=contact)
    address = AddressFactory.create(contact=contact)
    dates = SignificantDateFactory(contact=contact)
    socials = SocialMediaFactory.create_batch(3, contact=contact)

    contact_count = await Contact.all().count()
    phones_count = await Phone.all().count()

    assert contact_count == 1
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
