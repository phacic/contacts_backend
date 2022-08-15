from typing import Dict, List, Union

from pydantic import EmailStr, root_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from app.db.models.contact import (
    Address,
    Contact,
    ContactTag,
    Email,
    Phone,
    SignificantDate,
)

ContactTagSchema = pydantic_model_creator(ContactTag, name="ContactTag")
ContactTagCreateSchema = pydantic_model_creator(
    ContactTag, name="ContactTagCreate", exclude_readonly=True
)

AddressSchema = pydantic_model_creator(Address, name="Address")
AddressCreateSchema = pydantic_model_creator(
    Address, name="AddressCreateSchema", exclude_readonly=True
)

PhoneSchema = pydantic_model_creator(Phone, name="Phone")
PhoneCreateSchema = pydantic_model_creator(
    Phone, name="PhoneCreate", exclude_readonly=True
)

EmailSchema = pydantic_model_creator(Email, name="Email")
EmailCreateDefaultSchema = pydantic_model_creator(
    Email, name="EmailCreate", exclude_readonly=True
)


class EmailCreateSchema(EmailCreateDefaultSchema):
    email: EmailStr


SignificantDateSchema = pydantic_model_creator(SignificantDate, name="SignificantDate")
SignificantDateCreateSchema = pydantic_model_creator(
    SignificantDate, name="SignificantDateCreateSchema", exclude_readonly=True
)

ContactDefaultSchema = pydantic_model_creator(Contact, name="Contact")
ContactCreateDefaultSchema = pydantic_model_creator(
    Contact, name="ContactCreate", exclude_readonly=True, exclude=("status",)
)


class ContactSchema(ContactDefaultSchema):
    user_id: Union[None, int] = None
    phones: List[PhoneSchema]
    emails: List[EmailSchema]
    addresses: List[AddressSchema]
    significant_dates: List[SignificantDateSchema]


class ContactCreateSchema(ContactCreateDefaultSchema):
    phones: Union[None, List[PhoneCreateSchema]] = []
    emails: Union[None, List[EmailCreateSchema]] = []
    addresses: Union[None, List[AddressCreateSchema]] = []
    significant_dates: Union[None, List[SignificantDateCreateSchema]] = []

    @root_validator
    def check_firstname_phones(cls, values: Dict):
        """
        should at least have a phone number or a name
        """
        first_name, phones = values.get("first_name"), values.get("phones")
        if not any([first_name, phones]):
            raise ValueError(
                "contact should either have a phone number or first name associated"
            )

        return values
