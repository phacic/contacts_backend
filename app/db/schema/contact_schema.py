from tortoise.contrib.pydantic import pydantic_model_creator

from app.db.models.contact import (
    Contact, ContactTag, Phone, Email, SignificantDate
)


ContactSchema = pydantic_model_creator(Contact, name="Contact")
ContactCreateSchema = pydantic_model_creator(Contact, name="ContactCreate", exclude_readonly=True)

ContactTagSchema = pydantic_model_creator(ContactTag, name="ContactTag")
ContactTagCreateSchema = pydantic_model_creator(ContactTag, name="ContactTagCreate", exclude_readonly=True)

PhoneSchema = pydantic_model_creator(Phone, name="Phone")
PhoneCreateSchema = pydantic_model_creator(Phone, name="PhoneCreate", exclude_readonly=True)

EmailSchema = pydantic_model_creator(Email, name="Email")
EmailCreateSchema = pydantic_model_creator(Email, name="EmailCreate", exclude_readonly=True)

SignificantDateSchema = pydantic_model_creator(SignificantDate, "SignificantDate")
SignificantDateCreateSchema = pydantic_model_creator(SignificantDate, "SignificantDateCreateSchema",
                                                     exclude_readonly=True)