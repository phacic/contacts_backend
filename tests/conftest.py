from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def app_client() -> Generator[TestClient, None, None]:
    """
    fixture for raw app client (without running events)
    """
    yield TestClient(app)


@pytest.fixture
def app_client_startup() -> Generator[TestClient, None, None]:
    """
    fixture for app client that runs events (startup, shutdown)
    """
    with TestClient(app) as test_app:
        yield test_app
