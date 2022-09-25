from typing import Callable, Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer as tortoise_finalize
from tortoise.contrib.test import initializer as tortoise_init

from app.core.tortoise import MODEL_LIST
from app.main import app


@pytest.fixture
def app_client() -> Generator[TestClient, None, None]:
    """
    fixture for raw app client. If init is True run startup and shutdown events
    """
    yield TestClient(app)


@pytest.fixture
def app_client_events() -> Generator[TestClient, None, None]:
    """
    fixture for app client that runs events (startup, shutdown)
    """
    tortoise_init(modules=MODEL_LIST)
    with TestClient(app) as test_app:
        yield test_app

    tortoise_finalize()
