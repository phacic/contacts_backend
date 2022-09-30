import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.db.models import Contact
from tests.factory import ContactFactory


@pytest.mark.asyncio
async def test_root(app_client_events: TestClient) -> None:
    """
    test root redirect to docs
    """
    resp = app_client_events.get("/")

    print(resp.history)

    # should be redirect response with status 307
    assert resp.history[0].status_code == status.HTTP_307_TEMPORARY_REDIRECT

    # actual response should be 200
    assert resp.status_code == status.HTTP_200_OK

    # url after redirect should be /docs
    assert resp.request.path_url == "/docs"
