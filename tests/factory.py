import asyncio
from typing import Any

import factory
import nest_asyncio
from factory import base
from faker import Faker

from app.db.models import Address, Contact, Email, Phone, SignificantDate

fake = Faker()


class TortoiseModelFactory(base.Factory):
    """
    Base factory for tortoise factory.
    """

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

        instance = model_class(*args, **kwargs)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        async def save_instance(model_instance):
            await model_instance.save()

        if loop:
            # patch asyncio to allow nesting loops.
            # https://github.com/erdewit/nest_asyncio
            nest_asyncio.apply(loop=loop)

            # because of the patch a database connections lingers after the factory
            # is done and that prevents the database from closing after the tests.
            # unless Tortoise.connection.connections.close_all() is called from within the test,
            # the test teardown always fails, even with conftest teardown
            # RuntimeError: Task is attached to a different loop

            asyncio.get_event_loop().run_until_complete(save_instance(instance))

        else:
            asyncio.run(save_instance(instance))

        return instance


Labels = ["Work", "Home", "Main", "Other"]
Contact_labels = Labels + ["Mobile"]
Date_labels = ["Birthday", "Anniversary"]


class ContactFactory(TortoiseModelFactory):
    class Meta:
        model = Contact

    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    company = factory.Faker("company")
    note = factory.Faker("text")
    website = factory.Faker("url")
    spouse = factory.Faker("name")
    nickname = factory.Faker("name")
    is_favorite = factory.Faker("boolean")


class PhoneFactory(TortoiseModelFactory):
    class Meta:
        model = Phone

    phone_number = factory.Faker("phone_number")
    label = factory.Iterator(Contact_labels)
    contact = factory.SubFactory(ContactFactory)


class EmailFactory(TortoiseModelFactory):
    class Meta:
        model = Email

    email_address = factory.Faker("email")
    label = factory.Iterator(Labels)
    contact = factory.SubFactory(ContactFactory)


class SignificantDateFactory(TortoiseModelFactory):
    class Meta:
        model = SignificantDate

    date = factory.LazyFunction(fake.date)
    label = factory.Iterator(Date_labels)
    contact = factory.SubFactory(ContactFactory)


class AddressFactory(TortoiseModelFactory):
    class Meta:
        model = Address

    location = factory.Faker("address")
    label = factory.Iterator(Labels)
    contact = factory.SubFactory(ContactFactory)