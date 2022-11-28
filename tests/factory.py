import asyncio
import inspect
from typing import List

import factory
from factory import base
from faker import Faker
from fastapi_users.password import PasswordHelper
from tortoise import Model

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
Phone_Labels = Contact_labels
Email_Labels = Labels
Address_Labels = Labels
Date_Labels = ["Birthday", "Anniversary"]
Social_Labels = ["Twitter", "Facebook", "Instagram", "Snapchat", "LinkedIn"]


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

    user = factory.SubFactory(UserFactory)


class PhoneFactory(TModelFactory):
    class Meta:
        model = Phone

    phone_number = factory.Faker("phone_number")
    label = factory.Iterator(Phone_Labels)
    contact = factory.SubFactory(ContactFactory)


class EmailFactory(TModelFactory):
    class Meta:
        model = Email

    email_address = factory.Faker("email")
    label = factory.Iterator(Email_Labels)
    contact = factory.SubFactory(ContactFactory)


class SignificantDateFactory(TModelFactory):
    class Meta:
        model = SignificantDate

    date = factory.LazyFunction(fake.date)
    label = factory.Iterator(Date_Labels)
    contact = factory.SubFactory(ContactFactory)


class AddressFactory(TModelFactory):
    class Meta:
        model = Address

    location = factory.Faker("address")
    label = factory.Iterator(Address_Labels)
    contact = factory.SubFactory(ContactFactory)


class SocialMediaFactory(TModelFactory):
    class Meta:
        model = SocialMedia

    url = factory.Faker("uri")
    label = factory.Iterator(Social_Labels)
    contact = factory.SubFactory(ContactFactory)


async def refresh_from_db(instances: List[Model]) -> List[Model]:
    """
    call refresh_from_db on model instance
    """
    [await i.refresh_from_db() for i in instances]
    return instances

