from typing import List, Optional, Dict

from tortoise import fields, models
from fastapi_users.db.base import BaseUserDatabase
from fastapi_users.db import ObjectIDIDMixin
from fastapi_users_tortoise import TortoiseUserDatabase, TortoiseBaseUserAccountModel

from app.db.models.base import BaseModel, LabelMixin
from app.db.models.constant import ModelRelations, StatusOptions


class Contact(BaseModel):
    """
    contact model for a person contact
    """
    first_name = fields.CharField(max_length=60, null=True)
    middle_name = fields.CharField(max_length=60, null=True)
    last_name = fields.CharField(max_length=60, null=True)
    company = fields.CharField(max_length=120, null=True)
    note = fields.TextField(null=True)
    website = fields.CharField(max_length=120, null=True)
    spouse = fields.CharField(max_length=120, null=True)
    nickname = fields.CharField(max_length=60, null=True)
    # mark as favorite
    is_favorite = fields.BooleanField(default=False)
    # mark as hidden
    is_hidden = fields.BooleanField(default=False)
    # active, inactive (moved to recycle)
    # if set to inactive, no further changes will be allowed, so we can safely
    # use updated_at to check the date status change happened (to inactive)
    status = fields.CharField(max_length=2, default=StatusOptions.Active.value)
    tags = fields.ManyToManyField(model_name=ModelRelations.Tag.value, related_name="tags")

    # owner
    user = fields.ForeignKeyField(model_name=ModelRelations.User.value, related_name="contacts", null=True)

    # improve hinting
    phones: fields.ReverseRelation["Phone"]
    emails: fields.ReverseRelation["Email"]
    significant_dates: fields.ReverseRelation["SignificantDate"]

    def __str__(self):
        names = [str(self.first_name).strip(), str(self.middle_name).strip(), str(self.last_name).strip()]
        return f'{" ".join(names)}'.strip()


class ContactTag(BaseModel):
    """
    model for tags, for contacts, as a way of grouping contacts
    """
    tag = fields.CharField(max_length=15)
    contacts = fields.ManyToManyRelation["Contact"]

    def __str__(self):
        return self.tag


class Phone(LabelMixin, BaseModel):
    """
    model for phone numbers associated with a contact
    """
    phone_number = fields.CharField(max_length=15)
    contact = fields.ForeignKeyField(ModelRelations.Contact.value, related_name="phones")

    def __str__(self):
        return f'{self.label} - {self.phone_number}'


class Email(LabelMixin, BaseModel):
    """
    model for email addresses associated with a contact
    """
    email_address = fields.CharField(max_length=120)
    contact = fields.ForeignKeyField(ModelRelations.Contact.value, related_name="emails")

    def __str__(self):
        return F'{self.label} - {self.email_address}'


class SignificantDate(LabelMixin, BaseModel):
    """
    birthday, anniversary, e.t.c, associated with a contact
    """
    date = fields.DatetimeField()
    contact = fields.ForeignKeyField(ModelRelations.Contact.value, related_name="significant_dates")

    def __str__(self):
        return f'{self.label} - {self.date}'


class Address(LabelMixin, BaseModel):
    """
    address associated with Contact
    """
    location = fields.TextField()
    contact = fields.ForeignKeyField(ModelRelations.Contact.value, related_name="addresses")

    def __str__(self):
        return F'{self.label} - {self.location}'
