# import models here so tortoise can find them all under app.db.models

from app.db.models.contact import Email  # noqa
from app.db.models.contact import Phone  # noqa
from app.db.models.contact import Address, Contact, ContactTag, SignificantDate  # noqa
from app.db.models.user import User  # noqa
