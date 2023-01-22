from datetime import datetime
from typing import Dict, List, Union

from pydantic import EmailStr, constr, root_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from app.db.models.contact import (
    Address,
    Contact,
    ContactTag,
    Email,
    Phone,
    SignificantDate,
    SocialMedia,
)

ContactTagSchema = pydantic_model_creator(ContactTag, name="ContactTag")
ContactTagCreateSchema = pydantic_model_creator(
    ContactTag, name="ContactTagCreate", exclude_readonly=True
)

AddressSchema = pydantic_model_creator(Address, name="Address")
AddressCreateSchema = pydantic_model_creator(
    Address, name="AddressCreateSchema", exclude_readonly=True
)


class AddressUpdateSchema(AddressCreateSchema):
    location: Union[None, str] = None


PhoneSchema = pydantic_model_creator(Phone, name="Phone")
PhoneCreateSchema = pydantic_model_creator(
    Phone, name="PhoneCreate", exclude_readonly=True
)


class PhoneUpdateSchema(PhoneCreateSchema):
    id: Union[None, int] = None
    phone_number: Union[None, str] = None


EmailSchema = pydantic_model_creator(Email, name="Email")
EmailCreateDefaultSchema = pydantic_model_creator(
    Email, name="EmailCreate", exclude_readonly=True
)


class EmailCreateSchema(EmailCreateDefaultSchema):
    email_address: EmailStr = constr(max_length=120)


class EmailUpdateSchema(EmailCreateSchema):
    id: Union[None, int] = None
    email_address: Union[EmailStr, constr(max_length=120)] = None


SocialSchema = pydantic_model_creator(SocialMedia, name="Social")
SocialCreateSchema = pydantic_model_creator(
    SocialMedia, name="SocialCreateSchema", exclude_readonly=True
)


class SocialUpdateSchema(SocialCreateSchema):
    id: Union[None, int] = None
    url: Union[None, str] = None


SignificantDateSchema = pydantic_model_creator(SignificantDate, name="SignificantDate")
SignificantDateCreateSchema = pydantic_model_creator(
    SignificantDate, name="SignificantDateCreateSchema", exclude_readonly=True
)


class SignificantDateUpdateSchema(SignificantDateCreateSchema):
    id: Union[None, int] = None
    date: Union[None, datetime] = None


ContactDefaultSchema = pydantic_model_creator(Contact, name="Contact")
ContactCreateDefaultSchema = pydantic_model_creator(
    Contact, name="ContactCreate", exclude_readonly=True, exclude=("status",)
)


class ContactSchema(ContactDefaultSchema):
    user_id: Union[None, int] = None
    phones: List[PhoneSchema]
    phones: List[PhoneSchema]
    emails: List[EmailSchema]
    addresses: List[AddressSchema]
    significant_dates: List[SignificantDateSchema]
    socials: List[SocialSchema]


class ContactCreateSchema(ContactCreateDefaultSchema):
    """
    ContactCreateDefaultSchema with defined fields and a validator
    """

    phones: Union[None, List[PhoneCreateSchema]] = []
    emails: Union[None, List[EmailCreateSchema]] = []
    addresses: Union[None, List[AddressCreateSchema]] = []
    significant_dates: Union[None, List[SignificantDateCreateSchema]] = []
    socials: Union[None, List[SocialCreateSchema]] = []

    @root_validator
    def check_firstname_phones(cls, values: Dict) -> Dict:
        """
        should at least have a phone number or a name
        """
        first_name, phones = values.get("first_name"), values.get("phones")
        if not any([first_name, phones]):
            raise ValueError(
                "contact should either have a phone number or first name associated"
            )

        return values


class ContactUpdateSchema(ContactCreateSchema):
    """
    schema for updating a contact
    """

    phones: Union[None, List[PhoneUpdateSchema]] = []
    emails: Union[None, List[EmailUpdateSchema]] = []
    addresses: Union[None, List[AddressUpdateSchema]] = []
    significant_dates: Union[None, List[SignificantDateUpdateSchema]] = []
    socials: Union[None, List[SocialUpdateSchema]] = []

    @root_validator
    def check_firstname_phones(cls, values: Dict) -> Dict:
        """
        override validator to ignore it
        """
        return values
