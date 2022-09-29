import pytest
from fastapi.testclient import TestClient
from tortoise.connection import connections

from app.db.models import Contact
from tests.factory import ContactFactory


@pytest.mark.asyncio
async def test_create_contact(app_client_events: TestClient) -> None:
    """

    """
    contacts = ContactFactory.create_batch(2)
    db_count = await Contact.all().count()

    assert len(contacts) == 2
    assert db_count == 2

    conns = connections.all()
    await connections.close_all()