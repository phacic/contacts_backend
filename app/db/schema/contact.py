from typing import List, Optional, Union
from pydantic import EmailStr

from tortoise.contrib.pydantic import pydantic_model_creator

from app.db.models.contact import (
    Contact, ContactTag, Phone, Email, SignificantDate, Address
)

ContactTagSchema = pydantic_model_creator(ContactTag, name="ContactTag")
ContactTagCreateSchema = pydantic_model_creator(ContactTag, name="ContactTagCreate", exclude_readonly=True)

AddressSchema = pydantic_model_creator(Address, name="Address")
AddressCreateSchema = pydantic_model_creator(Address, name="AddressCreateSchema", exclude_readonly=True)

PhoneSchema = pydantic_model_creator(Phone, name="Phone")
PhoneCreateSchema = pydantic_model_creator(Phone, name="PhoneCreate", exclude_readonly=True)

EmailSchema = pydantic_model_creator(Email, name="Email")
EmailCreateDefaultSchema = pydantic_model_creator(Email, name="EmailCreate", exclude_readonly=True)


class EmailCreateSchema(EmailCreateDefaultSchema):
    email: EmailStr


SignificantDateSchema = pydantic_model_creator(SignificantDate, name="SignificantDate")
SignificantDateCreateSchema = pydantic_model_creator(SignificantDate, name="SignificantDateCreateSchema",
                                                     exclude_readonly=True)

ContactDefaultSchema = pydantic_model_creator(Contact, name="Contact")
ContactCreateDefaultSchema = pydantic_model_creator(Contact, name="ContactCreate", exclude_readonly=True)


class ContactSchema(ContactDefaultSchema):
    phones: Union[None, List[PhoneSchema]]
    emails: List[EmailSchema]
    addresses: List[AddressSchema]
    significant_dates: List[SignificantDateSchema]


class ContactCreateSchema(ContactCreateDefaultSchema):
    phones: List[PhoneCreateSchema]
    emails: List[EmailCreateSchema]
    addresses: List[AddressCreateSchema]
    significant_dates: List[SignificantDateCreateSchema]
