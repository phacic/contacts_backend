import asyncio
from typing import Generator, Coroutine, Callable, List, Union, TYPE_CHECKING, Type

import pytest
from fastapi.testclient import TestClient
from tortoise.connection import connections
from tortoise.contrib.test import finalizer as tortoise_finalize, initializer as tortoise_init
from faker import Faker
from fastapi_users.password import PasswordHelper

from app.core.config import settings
from app.core.tortoise import MODEL_LIST
from app.main import app
from app.db.models import Contact, User

if TYPE_CHECKING:
    from tortoise import BaseDBAsyncClient, Model

fake = Faker()


@pytest.fixture
def anyio_backend():
    """
    Specifying the backends to run on
    """
    return 'asyncio'


@pytest.fixture(scope='module')
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


@pytest.fixture(scope='module')
def app_client(evloop: asyncio.BaseEventLoop) -> Generator[TestClient, None, None]:
    """
    fixture for app client that runs events (startup, shutdown)
    """
    tortoise_init(modules=MODEL_LIST, db_url=settings.DB_URL, loop=evloop)
    with TestClient(app) as test_app:
        yield test_app

    tortoise_finalize()


@pytest.fixture(scope="module")
def passwd() -> str:
    return fake.password()


@pytest.fixture(scope="module")
def hashed_passwd(passwd) -> str:
    pass_helper = PasswordHelper()
    return pass_helper.hash(passwd)


class ModelFactoryFixtureHelper:
    def __init__(self, model: Type['Model']):
        self.model = model

    async def _create_model_obj(self, **kwargs) -> 'Model':
        instance = self.model(**kwargs)
        await instance.save()
        return instance

    async def _create_model_batch_objs(self, size: int, **kwargs) -> List['Model']:
        return [await self._create_model_obj(**kwargs) for _ in range(size)]

    async def create(self, size: int, **kwargs) -> Union['Model', List['Model']]:
        instances = await self._create_model_batch_objs(model=self.model, size=size, **kwargs)
        return instances[0] if size == 1 else instances


async def create_model_obj(model: Type['Model'], **kwargs) -> 'Model':
    instance = model(**kwargs)
    await instance.save()
    return instance


async def create_model_batch_objs(model: Type['Model'], size, **kwargs) -> List['Model']:
    return [await create_model_obj(model, **kwargs) for _ in range(size)]


async def create_model_objs_one_or_many(model: Type['Model'], size=1, **kwargs) -> Union['Model', List['Model']]:
    instances = await create_model_batch_objs(model=model, size=size, **kwargs)
    return instances[0] if size == 1 else instances


@pytest.fixture()
def user_factory(hashed_passwd) -> Callable[[int], Coroutine[None, None, Union[User, List[User]]]]:
    """
    user factory fixture
    """

    async def create_batch(size: int = 1):
        data = {
            "full_name": fake.name(),
            "email": fake.email(),
            "hashed_password": hashed_passwd
        }
        helper = ModelFactoryFixtureHelper(model=User)
        return await helper.create(size=size, **data)

    return create_batch


@pytest.fixture()
def contact_factory() -> Callable[[int], Coroutine[None, None, Union[Contact, List[Contact]]]]:
    """ create contact factory fixture"""

    async def create_batch(size: int = 1, **kwargs):
        helper = ModelFactoryFixtureHelper(model=User)
        return await helper.create(size=size)

    return create_batch
