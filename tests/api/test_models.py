import pytest
from fastapi.testclient import TestClient

from app.db.models import Contact, Phone
from tests.factory import (
    AddressFactory,
    ContactFactory,
    EmailFactory,
    PhoneFactory,
    SignificantDateFactory,
)


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


@pytest.mark.asyncio
async def test_create_phone(
    app_client_events: TestClient, close_connections: None
) -> None:
    """"""

    _ = close_connections

    contact = ContactFactory()
    phones = PhoneFactory.create_batch(2, contact=contact)
    emails = EmailFactory.create_batch(2, contact=contact)
    address = AddressFactory.create(contact=contact)
    dates = SignificantDateFactory(contact=contact)

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
