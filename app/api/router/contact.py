from typing import List

from fastapi import APIRouter, Depends, status

from app.api.deps import current_user
from app.db.crud import create_new_contact, get_user_contact, get_user_contacts
from app.db.models import Contact, User
from app.db.schema import ContactCreateSchema, ContactSchema

router = APIRouter()


@router.get(path="/", response_model=List[ContactSchema])
async def all_contacts(user: User = Depends(current_user)):
    """
    list contact created by a user
    """
    return await get_user_contacts(user_id=user.id)


@router.get(
    path="/{contact_id}", response_model=ContactSchema, status_code=status.HTTP_200_OK
)
async def get_contact(contact_id: int, user=Depends(current_user)):
    """
    return a single contact using its id
    """
    return await get_user_contact(user_id=user.id, contact_id=contact_id)


@router.post(
    path="/", response_model=ContactSchema, status_code=status.HTTP_201_CREATED
)
async def add_contact(contact: ContactCreateSchema, user: User = Depends(current_user)):
    """
    create a new contact for a user
    """
    contact_dict = contact.dict(exclude_unset=True)
    contact_dict["user"] = user
    created_contact = await create_new_contact(contact_dict)
    return await ContactSchema.from_tortoise_orm(created_contact)


@router.delete(path="/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, user: User = Depends(current_user)):
    """
    remove a contact using its ID. The contact status is set inactive, to
    be permanently removed after 30 days
    """
