from typing import Any, Dict, List, Optional, Type, Union

from tortoise.models import MODEL, in_transaction

from app.db.models import Address, Contact, Email, Phone, SignificantDate, SocialMedia
from app.db.models.constant import StatusOptions
from app.db.schema import ContactSchema


async def create_new_contact(data: Dict) -> Contact:
    """
    save a new contact
    """
    phones = data.pop("phones", [])
    emails = data.pop("emails", [])
    dates = data.pop("significant_dates", [])
    addresses = data.pop("addresses", [])
    socials = data.pop("socials", [])

    # use transaction to save the pieces
    async with in_transaction():
        # create contact
        contact_obj = await Contact.create(**data)

        # the components
        await create_contact_component(contact_obj, phones, Phone)
        await create_contact_component(contact_obj, emails, Email)
        await create_contact_component(contact_obj, dates, SignificantDate)
        await create_contact_component(contact_obj, addresses, Address)
        await create_contact_component(contact_obj, socials, SocialMedia)

        return await contact_obj


async def create_contact_component(
    c: Contact, model_data: List[Dict], model: Type["MODEL"]
) -> Any:
    """
    create contact component (phone, email, address, etc)

    Args:
        c: Contact to associate to
        model_data: List of Data to create component
        model: The model for the component. e.g. Phone, Email
    """
    assert model is not None

    comps = [model(contact=c, **d) for d in model_data]
    return await model.bulk_create(comps)


async def update_contact(user_id: int, contact_id: int, data: Dict) -> Union[None, Contact]:
    """
    update an existing contact
    if a component comes with an id, we are updating if not create a new

    """
    contact = (
        await Contact.active_objects()
        .filter(user_id=user_id, id=contact_id)
        .first()
    )

    if not contact:
        return None

    phones = data.pop("phones", [])
    emails = data.pop("emails", [])
    dates = data.pop("significant_dates", [])
    addresses = data.pop("addresses", [])
    socials = data.pop("socials", [])

    async with in_transaction():
        # update contact
        if data:
            await contact.update_from_dict(data=data)

        # update components
        await update_contact_component(c=contact, model_data=phones, model=Phone)
        await update_contact_component(c=contact, model_data=emails, model=Email)
        await update_contact_component(
            c=contact, model_data=dates, model=SignificantDate
        )
        await update_contact_component(c=contact, model_data=addresses, model=Address)
        await update_contact_component(c=contact, model_data=socials, model=SocialMedia)

        return await contact


async def update_contact_component(
    *, c: Contact, model_data: List[Dict], model: Type["MODEL"]
) -> Any:
    """
    update, delete, create new component.
    When the incoming data has an id and nothing else, it gets deleted.
    If an id is present and has more data, the component gets updated.
    if no id but has data, a new one is created

    Args:
        c: Contact to associate to
        model_data: List of Data to create component
        model: The model for the component. e.g. Phone, Email
    """

    to_create = []
    for d in model_data:
        # when id is present,
        #   and it has more data, update
        #   if not delete
        # when id is absent but has more data, create new
        if item_id := d.pop("id", None):
            if len(d) > 0:
                await model.filter(id=item_id).update(**d)
            else:
                await model.filter(id=item_id).delete()

        # create new
        else:
            to_create.append(d)

    # create new ones
    if to_create:
        await create_contact_component(c=c, model_data=to_create, model=model)


async def get_user_contact(user_id: int, contact_id: int) -> Optional[Contact]:
    """
    get a contact created by a user
    """
    qs = Contact.filter(id=contact_id, user_id=user_id).first()
    return await ContactSchema.from_queryset_single(qs)


async def get_user_contacts(user_id: Optional[int] = None) -> List[Contact]:
    """
    contacts created by a user
    """
    qs = (
        Contact.active_objects()
        .filter(user_id=user_id)
        .prefetch_related(
            "phones", "emails", "significant_dates", "addresses", "socials"
        )
    )
    return await ContactSchema.from_queryset(qs)


async def deactivate_contact(user_id: int, contact_id: int) -> None:
    """
    set a contact status to inactive
    """
    await Contact.active_objects().filter(user_id=user_id, id=contact_id).update(
        status=StatusOptions.Inactive.value
    )
