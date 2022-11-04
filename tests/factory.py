import asyncio
import inspect

import factory
from factory import base
from faker import Faker
from fastapi_users.password import PasswordHelper

from app.db.models import (
    Address,
    Contact,
    Email,
    Phone,
    SignificantDate,
    SocialMedia,
    User,
)

fake = Faker()
passwd_helper = PasswordHelper()
passwd = fake.password()
hashed_passwd = passwd_helper.hash(passwd)


# class TortoiseModelFactory(base.Factory):
#     """
#     Base factory for tortoise factory.
#     """
#
#     class Meta:
#         abstract = True
#
#     @classmethod
#     def _create(cls, model_class, *args: Any, **kwargs: Any):
#         """
#         Creates an instance of Tortoise model.
#
#         :param model_class: model class.
#         :param args: factory args.
#         :param kwargs: factory keyword-args.
#         :return: instance of model class.
#         """
#
#         instance = model_class(*args, **kwargs)
#
#         try:
#             loop = asyncio.get_running_loop()
#         except RuntimeError:
#             loop = None
#
#         async def save_instance(model_instance):
#             await model_instance.save()
#
#         if loop:
#             # patch asyncio to allow nesting loops.
#             # https://github.com/erdewit/nest_asyncio
#             nest_asyncio.apply(loop=loop)
#
#             # because of the patch a database connections lingers after the factory
#             # is done and that prevents the database from closing after the tests.
#             # unless Tortoise.connection.connections.close_all() is called from within the test,
#             # the test teardown always fails, even with conftest teardown
#             # RuntimeError: Task is attached to a different loop
#
#             asyncio.get_event_loop().run_until_complete(save_instance(instance))
#
#         else:
#             asyncio.run(save_instance(instance))
#
#         return instance


class TModelFactory(base.Factory):
    def __init__(self, event_loop: asyncio.AbstractEventLoop):
        self.loop = event_loop

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        use async to create
        """

        async def do_create():
            nonlocal model_class
            nonlocal args
            nonlocal kwargs

            # SubFactories with return coroutine, await value
            # and pass back to kwargs
            for key, value in kwargs.items():
                if inspect.isawaitable(value):
                    kwargs[key] = await value

            instance = model_class(*args, **kwargs)
            await instance.save()
            return instance

        return do_create()

    @classmethod
    def create_batch(cls, size, **kwargs):
        """
        use async to create batch
        """

        async def do_create_batch():
            nonlocal size
            nonlocal kwargs

            return [await cls.create(**kwargs) for _ in range(size)]

        return do_create_batch()

    @classmethod
    def call_create(cls, kwargs=None):
        """
        so we can safely pass **kwargs from BlockingPortal.call()
        to cls.create()
        """
        kwargs = kwargs or {}
        return cls.create(**kwargs)

    @classmethod
    def call_create_batch(cls, size, kwargs=None):
        """
        so we can safely pass **kwargs from BlockingPortal.call()
        to cls.create_batch()
        """
        kwargs = kwargs or {}
        return cls.create_batch(size, **kwargs)


Labels = ["Work", "Home", "Main", "Other"]
Contact_labels = Labels + ["Mobile"]
Date_labels = ["Birthday", "Anniversary"]
social_labels = ["Twitter", "Facebook", "Instagram", "Snapchat", "LinkedIn"]


class UserFactory(TModelFactory):
    class Meta:
        model = User

    full_name = factory.Faker("name")
    email = factory.Faker("email")
    hashed_password = factory.LazyFunction(lambda: passwd_helper.hash(passwd))


class ContactFactory(TModelFactory):
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

    # >    if value and not value._saved_in_db:
    # E    AttributeError: 'coroutine' object has no attribute '_saved_in_db'
    user = factory.SubFactory(UserFactory)


class PhoneFactory(TModelFactory):
    class Meta:
        model = Phone

    phone_number = factory.Faker("phone_number")
    label = factory.Iterator(Contact_labels)
    contact = factory.SubFactory(ContactFactory)


class EmailFactory(TModelFactory):
    class Meta:
        model = Email

    email_address = factory.Faker("email")
    label = factory.Iterator(Labels)
    contact = factory.SubFactory(ContactFactory)


class SignificantDateFactory(TModelFactory):
    class Meta:
        model = SignificantDate

    date = factory.LazyFunction(fake.date)
    label = factory.Iterator(Date_labels)
    contact = factory.SubFactory(ContactFactory)


class AddressFactory(TModelFactory):
    class Meta:
        model = Address

    location = factory.Faker("address")
    label = factory.Iterator(Labels)
    contact = factory.SubFactory(ContactFactory)


class SocialMediaFactory(TModelFactory):
    class Meta:
        model = SocialMedia

    url = factory.Faker("uri")
    label = factory.Iterator(social_labels)
    contact = factory.SubFactory(ContactFactory)
