# import models here so tortoise can find them all under app.db.models

from app.db.models.contact import (
    Address,
    Contact,
    ContactTag,
    SignificantDate,
    SocialMedia,
    Email,
    Phone
)  # noqa
from app.db.models.user import User  # noqa
