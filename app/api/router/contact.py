from typing import List, Optional, Union

from fastapi import APIRouter, Body, Depends, Path, Query, status, HTTPException

from app.api.deps import current_user
from app.db.crud import (
    create_new_contact,
    deactivate_contact,
    get_user_contact,
    get_user_contacts,
    update_contact,
)
from app.db.models import Contact, User
from app.db.schema import ContactCreateSchema, ContactSchema, ContactUpdateSchema

router = APIRouter()


@router.get(path="/", response_model=List[ContactSchema])
async def all_contacts(user: User = Depends(current_user)) -> Optional[List[Contact]]:
    """
    list contact created by a user
    """
    return await get_user_contacts(user_id=user.id)


@router.get(
    path="/{contact_id}", response_model=ContactSchema, status_code=status.HTTP_200_OK
)
async def get_contact(
    contact_id: int = Path(..., title="ID of the contact"), user=Depends(current_user)
) -> Optional[Contact]:
    """
    return a single contact using its id
    """
    contact = await get_user_contact(user_id=user.id, contact_id=contact_id)
    if not contact:
        raise HTTPException(404, detail="Contact does not exit.")

    return contact


@router.post(
    path="/", response_model=ContactSchema, status_code=status.HTTP_201_CREATED
)
async def add_contact(
    contact: ContactCreateSchema, user: User = Depends(current_user)
) -> ContactSchema:
    """
    create a new contact for a user
    """
    contact_dict = contact.dict(exclude_unset=True)
    contact_dict["user"] = user
    created_contact = await create_new_contact(contact_dict)
    return await ContactSchema.from_tortoise_orm(created_contact)


@router.delete(path="/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(
    q: List[int] = Query(..., title="Contact IDs to remove"),
    user: User = Depends(current_user),
) -> None:
    """
    remove a contact using its ID. The contact status is set inactive, to
    be permanently removed after 30 days
    """
    for contact_id in q:
        await deactivate_contact(user_id=user.id, contact_id=contact_id)


@router.patch(
    path="/{contact_id}", response_model=ContactSchema, status_code=status.HTTP_200_OK
)
async def patch_contact(
    contact_id: int = Path(..., title="ID of contact to update"),
    contact: ContactUpdateSchema = Body(...),
    user: User = Depends(current_user),
) -> Union[HTTPException, ContactSchema]:
    """
    update an existing contact.
    Contact component (phone, email, etc) with id and one or more fields will be updated,
    while those with only id will be deleted. Those without ids will be created16
    ```{
        id: 1,
        first_name: Jonny
        phones: [
            {
                id: 1
                phone_number: ########
            }
            {
                id: 2
            },
            {
                phone_number: #####
                label: Mobile
            }
        ]
    }```
    """
    contact_dict = contact.dict(exclude_unset=True)
    updated_contact = await update_contact(
        user_id=user.id, contact_id=contact_id, data=contact_dict
    )
    if not updated_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact does not exist.")

    return await ContactSchema.from_tortoise_orm(updated_contact)
