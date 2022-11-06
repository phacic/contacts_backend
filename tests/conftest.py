import asyncio
from typing import (
    TYPE_CHECKING,
    Callable,
    Coroutine,
    Generator,
    List,
    Tuple,
    Type,
    Union,
)

import pytest
from anyio.from_thread import BlockingPortal
from faker import Faker
from fastapi import Response
from fastapi.testclient import TestClient
from fastapi_users.authentication.transport.bearer import BearerResponse
from pytest_factoryboy import register
from tortoise.connection import connections
from tortoise.contrib.test import finalizer as tortoise_finalize
from tortoise.contrib.test import initializer as tortoise_init

from app.core.config import settings
from app.core.tortoise import MODEL_LIST
from app.db.models import Contact, User
from app.internal import get_jwt_strategy, jwt_auth_backend
from app.main import app
from tests.factory import (
    AddressFactory,
    EmailFactory,
    PhoneFactory,
    SignificantDateFactory,
    SocialMediaFactory,
    UserFactory,
    hashed_passwd,
)

if TYPE_CHECKING:
    from tortoise import Model

fake = Faker()

# register Factories as fixtures
register(UserFactory)
register(PhoneFactory)
register(EmailFactory)
register(AddressFactory)
register(SignificantDateFactory)
register(SocialMediaFactory)


@pytest.fixture
def anyio_backend():
    """
    Specifying the backends to run on
    """
    return "asyncio"


@pytest.fixture(scope="module")
def evloop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def close_connections() -> Generator:
    """
    close open connection to db in the current loop or the final teardown fails
    with RuntimeError: Task attached to a different loop
    """

    yield
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connections.close_all())


@pytest.fixture(scope="module")
def init_database(evloop: asyncio.BaseEventLoop) -> Generator:
    """
    create database on start and drop on end
    """
    tortoise_init(modules=MODEL_LIST, db_url=settings.DB_URL, loop=evloop)
    yield
    tortoise_finalize()


@pytest.fixture(scope="module")
def app_client(
    evloop: asyncio.BaseEventLoop, init_database
) -> Generator[TestClient, None, None]:
    """
    fixture for app client that runs events (startup, shutdown).
    include init_database fixture to create database on start and drop it on end
    """
    with TestClient(app) as test_app:
        yield test_app


@pytest.fixture(scope="module")
def app_portal(app_client: TestClient) -> Generator[BlockingPortal, None, None]:
    """
    Blocking portal to use to call async functions
    """
    yield app_client.portal


class FixtureFactoryBaseMeta:
    abstract = True
    model = None


class ModelFactoryFixtureHelper:
    """
    Helper class for create fixture model objs
    """

    _meta = {}

    class Meta(FixtureFactoryBaseMeta):
        pass

    def __init__(self, model: Type["Model"]):
        self.model = model

    def __call__(self, size=1, **kwargs):
        return self.create(size, **kwargs)

    async def _create_model_obj(self, **kwargs) -> "Model":
        instance = self.model(**kwargs)
        await instance.save()
        return instance

    async def _create_model_batch_objs(self, size: int, **kwargs) -> List["Model"]:
        return [await self._create_model_obj(**kwargs) for _ in range(size)]

    async def create(self, size: int = 1, **kwargs) -> Union["Model", List["Model"]]:
        instances = await self._create_model_batch_objs(
            model=self.model, size=size, **kwargs
        )
        return instances[0] if size == 1 else instances


@pytest.fixture()
def user_factory_2() -> Callable[[int], Coroutine[None, None, Union[User, List[User]]]]:
    """
    user factory fixture
    """

    async def create_batch(size: int = 1):
        data = {
            "full_name": fake.name(),
            "email": fake.email(),
            "hashed_password": hashed_passwd,
        }
        helper = await ModelFactoryFixtureHelper(model=User)
        return await helper.create(size=size, **data)

    return create_batch


@pytest.fixture()
def contact_factory_2() -> Callable[
    [int], Coroutine[None, None, Union[Contact, List[Contact]]]
]:
    """create contact factory fixture"""

    async def create_batch(size: int = 1, **kwargs):
        helper = ModelFactoryFixtureHelper(model=User)
        return await helper.create(size=size)

    return create_batch


@pytest.fixture()
def logged_in_user(user_factory, app_portal) -> Generator[Tuple[str, User], None, None]:
    """
    log a user in and return token and user
    """
    user = app_portal.call(user_factory)

    strategy = get_jwt_strategy()
    resp = Response()
    bearer_resp: BearerResponse = app_portal.call(
        jwt_auth_backend.login, *(strategy, user, resp)
    )

    yield bearer_resp.access_token, user
