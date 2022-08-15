from typing import List

from fastapi import APIRouter

from app.db.crud import create_new_contact
from app.db.models import Contact
from app.db.schema import ContactCreateSchema, ContactSchema

router = APIRouter(tags=["Contact"])


@router.get(path="/", response_model=List[ContactSchema])
async def all_contacts():
    qs = Contact.all().prefetch_related(
        "phones", "emails", "significant_dates", "addresses"
    )
    return await ContactSchema.from_queryset(qs)


@router.post(path="/", response_model=ContactSchema)
async def add_contact(contact: ContactCreateSchema):
    contact_dict = contact.dict(exclude_unset=True)
    created_contact = await create_new_contact(contact_dict)
    return await ContactSchema.from_tortoise_orm(created_contact)
