import json
from typing import Callable, List, Tuple

import pytest
from anyio.from_thread import BlockingPortal
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

from app.db.models import Contact, User
from app.db.models.constant import StatusOptions
from tests.factory import (
    Address_Labels,
    Date_Labels,
    Email_Labels,
    Phone_Labels,
    Social_Labels,
    passwd,
    refresh_from_db
)

fake = Faker()


@pytest.mark.anyio
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


@pytest.mark.anyio
class TestUserRoute:
    async def test_register(self, app_client: TestClient) -> None:
        reg_data = {
            "full_name": fake.name(),
            "email": fake.email(),
            "password": fake.password(),
        }

        resp = app_client.post(url="/auth/register", data=json.dumps(reg_data))
        resp_data = resp.json()
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["status"] == "A"

    async def test_login(self, app_client: TestClient, user_factory) -> None:
        user = app_client.portal.call(user_factory)

        payload = {"username": user.email, "password": passwd}

        resp = app_client.post(url="/auth/login", data=payload, headers={}, files=[])
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["access_token"] is not None


@pytest.mark.anyio
class TestContactRoute:
    async def test_create_contact(
        self, app_client: TestClient, logged_in_user: Tuple[str, User]
    ) -> None:
        """ """
        token, user = logged_in_user
        payload = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phones": [
                {
                    "phone_number": fake.phone_number(),
                    "label": fake.random_choices(Phone_Labels, 1)[0],
                },
                {
                    "phone_number": fake.phone_number(),
                    "label": fake.random_choices(Phone_Labels, 1)[0],
                },
            ],
            "emails": [
                {
                    "email_address": fake.email(),
                    "label": fake.random_choices(Email_Labels, 1)[0],
                }
            ],
            "addresses": [
                {
                    "location": fake.address(),
                    "label": fake.random_choices(Address_Labels, 1)[0],
                }
            ],
            "significant_dates": [
                {
                    "date": fake.date_time().isoformat(),
                    "label": fake.random_choices(Date_Labels, 1)[0],
                }
            ],
            "socials": [
                {"url": fake.url(), "label": fake.random_choices(Social_Labels, 1)[0]},
                {"url": fake.url(), "label": fake.random_choices(Social_Labels, 1)[0]},
            ],
        }

        headers = {"Authorization": f"Bearer {token}"}

        resp = app_client.post(
            url="/api/v1/contact/", data=json.dumps(payload), headers=headers
        )
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED

        # contact should be associated to the user
        assert resp_data["user_id"] == user.id

        # counting
        assert len(resp_data["phones"]) == 2
        assert len(resp_data["emails"]) == 1
        assert len(resp_data["addresses"]) == 1
        assert len(resp_data["significant_dates"]) == 1
        assert len(resp_data["socials"]) == 2

    async def test_get_user_contacts(
        self,
        app_client: TestClient,
        create_contacts: Callable[[int], List[Contact]],
        logged_in_user: Tuple[str, User],
    ) -> None:
        """
        test fetching contacts for a user
        """

        token, user = logged_in_user
        headers = {"Authorization": f"Bearer {token}"}

        # create contacts
        cl = create_contacts(6)

        resp = app_client.get(url="/api/v1/contact", headers=headers)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp_data) == len(cl)

    async def test_get_single_user_contact(
        self,
        app_client: TestClient,
        create_contacts: Callable[[int], List[Contact]],
        logged_in_user: Tuple[str, User],
    ) -> None:
        """
        test fetching a single contact
        """
        token, user = logged_in_user
        headers = {"Authorization": f"Bearer {token}"}

        # create contacts
        cl = create_contacts(2)

        first_id = cl[0].id
        url = f"/api/v1/contact/{first_id}"
        resp = app_client.get(url=url, headers=headers)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["id"] == first_id

    async def test_remove_contact(
        self,
        app_client: TestClient,
        app_portal: BlockingPortal,
        create_contacts: Callable[[int], List[Contact]],
        logged_in_user: Tuple[str, User]
    ) -> None:

        token, user = logged_in_user
        headers = {"Authorization": f"Bearer {token}"}

        # create contacts
        cl = create_contacts(2)

        # ?q=1&q=2
        query = "".join(f"q={c.id}&" for c in cl)
        url = f"/api/v1/contact/?{query}"
        resp = app_client.delete(url=url, headers=headers)

        assert resp.status_code == status.HTTP_204_NO_CONTENT

        # status should be changed to inactive
        cl = app_portal.call(refresh_from_db, *(cl,))
        for c in cl:
            assert c.status == StatusOptions.Inactive
