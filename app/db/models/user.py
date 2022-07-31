from tortoise import fields

from app.db.models.base import BaseModel


class User(BaseModel):
    """
    (make-shift) User model
    """
    fullname = fields.CharField(max_length=120, null=True)
    username = fields.CharField(30)
    email = fields.CharField(120)
    password = fields.CharField(90)

    class PydanticMeta:
        exclude = ('password', )

    def __str__(self):
        return self.fullname or self.username
