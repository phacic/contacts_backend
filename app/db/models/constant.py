from enum import Enum


class ModelRelations(str, Enum):
    """
    model relations
    """

    Contact = "models.Contact"
    Tag = "models.ContactTag"
    User = "models.User"


class StatusOptions(str, Enum):
    """ """

    Active = "A"
    Inactive = "I"
