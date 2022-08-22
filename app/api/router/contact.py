from typing import List

from fastapi import APIRouter, Depends

from app.db.crud import create_new_contact
from app.db.models import Contact, User
from app.db.schema import ContactCreateSchema, ContactSchema
from app.api.deps import current_user

router = APIRouter()


@router.get(path="/", response_model=List[ContactSchema])
async def all_contacts(user: User = Depends(current_user)):
    """
    list contact created by a user
    """
    qs = Contact.filter(user=user).prefetch_related(
        "phones", "emails", "significant_dates", "addresses"
    )
    return await ContactSchema.from_queryset(qs)


@router.post(path="/", response_model=ContactSchema)
async def add_contact(contact: ContactCreateSchema, user: User = Depends(current_user)):
    """
    create a new contact for a user
    """
    contact_dict = contact.dict(exclude_unset=True)
    contact_dict["user"] = user
    created_contact = await create_new_contact(contact_dict)
    return await ContactSchema.from_tortoise_orm(created_contact)
