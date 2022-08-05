from enum import Enum, IntEnum


class ModelRelations(str, Enum):
    """
    model relations
    """
    Contact = 'models.Contact'
    Tags = 'models.ContactTag'


class StatusOptions(str, Enum):
    """

    """
    Active = "A"
    Inactive = "I"


# class BaseLabelOptions(str, Enum):
#     """
#     basic label options
#     """
#     work = "Work"
#     personal = "Personal"
#     other = "other"
#
#
# class PhoneLabelOptions(BaseLabelOptions):
#     """
#     label for phone
#     """
#     mobile = "Mobile"
#     home = "Home"
#
#
# class EmailLabelOptions(BaseLabelOptions):
#     """
#     label for emails
#     """
#     pass
#
#
# class AddressLabelOptions(BaseLabelOptions):
#     """
#     label for address
#     """
#     pass
#
#
# class SignificantDateLabelOptions(str, Enum):
#     """
#     label for dates
#     """
#     birthday = "Birthday"
#     anniversary = "Anniversary"
