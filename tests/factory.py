import asyncio
from asyncio.exceptions import InvalidStateError
from typing import Any

import factory
from factory import base
import nest_asyncio

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

        nest_asyncio.apply(loop)
        asyncio.run(save_instance(instance=model_instance))
        return model_instance



class ContactFactory(TortoiseModelFactory):
    class Meta:
        model = Contact

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
