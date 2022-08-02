from typing import List
from fastapi import APIRouter

from app.db.models import Contact
from app.db.schema import (
    ContactCreateSchema, ContactSchema
)

router = APIRouter(tags=["Contact"])


@router.get(path="/", response_model=List[ContactSchema])
async def all_contacts():
    return await ContactSchema.from_queryset(Contact.all())
    # return []


@router.post(path="/", response_model=ContactSchema)
async def create_contact(contact: ContactCreateSchema):
    contact_dict = contact.dict(exclude_unset=True)
    created_contact = await Contact.create(**contact_dict)
    return await ContactSchema.from_tortoise_orm(created_contact)
