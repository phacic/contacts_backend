# import models here so tortoise can find them all under app.db.models

from app.db.models.contact import (
    Contact, ContactTag, Email, Phone, SignificantDate, Address
)
from app.db.models.user import User
