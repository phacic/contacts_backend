import pytest
from fastapi.testclient import TestClient

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


@pytest.mark.asyncio
async def test_create_user(app_client_events: TestClient, close_connections: None) -> None:
    _ = close_connections

    user = UserFactory.create()
    db_count = await User.all().count()

    assert user is not None
    assert db_count == 1


@pytest.mark.asyncio
async def test_create_contact(
    app_client_events: TestClient, close_connections: None
) -> None:
    """ """
    _ = close_connections

    contacts = ContactFactory.create_batch(2)
    db_count = await Contact.all().count()

    assert len(contacts) == 2
    assert db_count == 2

    for c in contacts:
        assert c.user_id is not None


@pytest.mark.asyncio
async def test_contact_with_details(
    app_client_events: TestClient, close_connections: None
) -> None:
    """"""

    _ = close_connections

    contact = ContactFactory()
    phones = PhoneFactory.create_batch(2, contact=contact)
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
