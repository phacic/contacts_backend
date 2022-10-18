import json

import pytest
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from tortoise.connection import connections

from tests.factory import passwd, UserFactory

fake = Faker()


@pytest.mark.asyncio
async def test_root_route(app_client: TestClient) -> None:
    """
    test root redirect to docs
    """
    resp = app_client.get("/")

    print(resp.history)

    # should be redirect response with status 307
    assert resp.history[0].status_code == status.HTTP_307_TEMPORARY_REDIRECT

    # actual response should be 200
    assert resp.status_code == status.HTTP_200_OK

    # url after redirect should be /docs
    assert resp.request.path_url == "/docs"


@pytest.mark.asyncio
class TestUserRoute:

    async def test_register(self, app_client: TestClient) -> None:

        reg_data = {
            "full_name": fake.name(),
            "email": fake.email(),
            "password": fake.password()
        }

        resp = app_client.post(url="/auth/register", data=json.dumps(reg_data))
        resp_data = resp.json()
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data['status'] == 'A'

    async def test_login(self, app_client: TestClient, close_connections: None) -> None:
        _ = close_connections

        user = UserFactory()
        await connections.close_all()

        payload = {
            "username": user.email,
            "password": passwd
        }

        resp = app_client.post(url="/auth/login", data=payload, headers={}, files=[])
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data['access_token'] is not None