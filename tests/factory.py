import asyncio
from typing import Any

import factory
import nest_asyncio
from factory import base

from app.db.models import Contact


class TortoiseModelFactory(base.Factory):
    """Base factory for tortoise factory."""

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args: Any, **kwargs: Any):
        """
        Creates an instance of Tortoise model.

        :param model_class: model class.
        :param args: factory args.
        :param kwargs: factory keyword-args.
        :return: instance of model class.
        """

        model_instance = model_class(*args, **kwargs)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        async def save_instance(instance):
            await instance.save()

        # because of the patch a database connections lingers after the factory
        # is done and that prevents the database from closing after the tests
        # unless connections.close_all() is called from within the test, the test
        # teardown always fails, even with conftest teardown
        # RuntimeError: Task is attached to a different loop

        nest_asyncio.apply(loop)
        # asyncio.run(save_instance(instance=model_instance))
        asyncio.get_event_loop().run_until_complete(save_instance(model_instance))
        return model_instance


class ContactFactory(TortoiseModelFactory):
    class Meta:
        model = Contact

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
