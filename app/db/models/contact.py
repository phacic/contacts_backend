from typing import List, Optional, Dict

from tortoise import fields

from app.db.models.base import BaseModel, LabelMixin
from app.db.models.constant import CONTACT, USER


class Contact(LabelMixin, BaseModel):
    """
    contact model for a person contact
    """
    user = fields.ForeignKeyField(USER, related_name="contacts")
    first_name = fields.CharField(max_length=60, null=True)
    middle_name = fields.CharField(max_length=60, null=True)
    last_name = fields.CharField(max_length=60, null=True)
    company = fields.CharField(max_length=120, null=True)
    address = fields.TextField(null=True)
    note = fields.TextField(null=True)
    website = fields.CharField(max_length=120, null=True)
    spouse = fields.CharField(max_length=120)
    nickname = fields.CharField(max_length=60)
    # mark as favorite
    is_favorite = fields.BooleanField(default=False)
    # mark as hidden
    is_hidden = fields.BooleanField(default=False)
    # active, inactive (moved to recycle)
    # if set to inactive, no further changes will be allowed, so we can safely
    # use updated_at to check the date status change happened (to inactive)
    status = fields.CharField(max_length=2)

    def __str__(self):
        names = [str(self.first_name).strip(), str(self.middle_name).strip(), str(self.last_name).strip()]
        label = f'({self.label})' if self.label else ''
        return f'{" ".join(names)} {label}'.strip()


class ContactTag(BaseModel):
    """
    model for tags, for contacts, as a way of grouping contacts
    """
    tag = fields.CharField(max_length=15)
    contact = fields.ForeignKeyField(CONTACT, related_name="tags")

    def __str__(self):
        return self.tag


class Phone(LabelMixin, BaseModel):
    """
    model for phone numbers associated with a contact
    """
    phone_number = fields.CharField(max_length=15)
    contact = fields.ForeignKeyField(CONTACT, related_name="phones")

    def __str__(self):
        return f'{self.phone_number} - {self.label}'


class Email(LabelMixin, BaseModel):
    """
    model for email addresses associated with a contact
    """
    email_address = fields.CharField(max_length=120)
    contact = fields.ForeignKeyField(CONTACT, related_name="emails")

    def __str__(self):
        return f'{self.email_address} - {self.label}'


class SignificantDate(LabelMixin, BaseModel):
    """
    birthday, anniversary, e.t.c, associated with a contact
    """
    date = fields.DatetimeField()
    contact = fields.ForeignKeyField(CONTACT, related_name="significant_dates")

    def __str__(self):
        return f'{self.date} - {self.label}'
