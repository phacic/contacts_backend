from tortoise import fields

from app.db.models.base import BaseModel, LabelMixin
from app.db.models.constant import ModelRelations, StatusOptions
from app.db.models.user import User


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
    # which will be useful to permanently delete a contact that has been marked
    # inactive over a period of time
    status = fields.CharField(max_length=2, default=StatusOptions.Active.value)
    tags: fields.ManyToManyRelation["ContactTag"] = fields.ManyToManyField(
        model_name=ModelRelations.Tag.value, related_name="tags"
    )

    # owner
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name=ModelRelations.User.value, related_name="contacts", null=True
    )

    # improve hinting
    phones: fields.ReverseRelation["Phone"]
    emails: fields.ReverseRelation["Email"]
    significant_dates: fields.ReverseRelation["SignificantDate"]
    addresses: fields.ReverseRelation["Address"]
    socials: fields.ReverseRelation["SocialMedia"]

    def __str__(self):
        names = [
            str(self.first_name or "").strip(),
            str(self.middle_name or "").strip(),
            str(self.last_name or "").strip(),
        ]
        return f'{" ".join(names)}'.strip()

    async def save(
        self,
        using_db=None,
        update_fields=None,
        force_create: bool = False,
        force_update: bool = False,
    ) -> None:
        await super(Contact, self).save(
            using_db=using_db,
            update_fields=update_fields,
            force_create=force_create,
            force_update=force_update,
        )


class ContactTag(BaseModel):
    """
    model for tags, for contacts, as a way of grouping contacts
    """

    tag = fields.CharField(max_length=50)
    contacts: fields.ManyToManyRelation[Contact] = fields.ManyToManyRelation["Contact"]

    def __str__(self):
        return self.tag


class Phone(LabelMixin, BaseModel):
    """
    model for phone numbers associated with a contact
    """

    phone_number = fields.CharField(max_length=50)
    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField(
        ModelRelations.Contact.value, related_name="phones"
    )

    def __str__(self) -> str:
        return f"{self.label} - {self.phone_number}"


class Email(LabelMixin, BaseModel):
    """
    model for email addresses associated with a contact
    """

    email_address = fields.CharField(max_length=120)
    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField(
        ModelRelations.Contact.value, related_name="emails"
    )

    def __str__(self) -> str:
        return f"{self.label} - {self.email_address}"


class SignificantDate(LabelMixin, BaseModel):
    """
    birthday, anniversary, e.t.c, associated with a contact
    """

    date = fields.DatetimeField()
    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField(
        ModelRelations.Contact.value, related_name="significant_dates"
    )

    def __str__(self) -> str:
        return f"{self.label} - {self.date}"


class Address(LabelMixin, BaseModel):
    """
    address associated with Contact
    """

    location = fields.TextField()
    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField(
        ModelRelations.Contact.value, related_name="addresses"
    )

    def __str__(self) -> str:
        return f"{self.label} - {self.location}"


class SocialMedia(LabelMixin, BaseModel):
    """
    social media links for the contact
    """

    contact: fields.ForeignKeyRelation[Contact] = fields.ForeignKeyField(
        ModelRelations.Contact.value, related_name="socials"
    )
    url = fields.CharField(max_length=255)

    def __str__(self):
        return f"{self.label} - {self.url}"
