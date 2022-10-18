import asyncio
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.connection import connections
from tortoise.contrib.test import finalizer as tortoise_finalize
from tortoise.contrib.test import initializer as tortoise_init

from app.core.config import settings
from app.core.tortoise import MODEL_LIST
from app.main import app


@pytest.fixture
def close_connections() -> Generator:
    """
    close open connection to db in the current loop or the final teardown fails
    with RuntimeError: Task attached to a different loop
    """

    yield
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connections.close_all())


@pytest.fixture
def app_client_() -> Generator[TestClient, None, None]:
    """
    fixture for raw app client. If init is True run startup and shutdown events
    """
    yield TestClient(app)


@pytest.fixture
def app_client() -> Generator[TestClient, None, None]:
    """
    fixture for app client that runs events (startup, shutdown)
    """
    tortoise_init(modules=MODEL_LIST, db_url=settings.DB_URL)
    with TestClient(app) as test_app:
        yield test_app

    tortoise_finalize()

