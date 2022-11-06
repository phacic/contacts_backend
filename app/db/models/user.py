from fastapi_users_tortoise import TortoiseBaseUserAccountModel
from tortoise import fields, timezone

from app.db.models.constant import StatusOptions


class User(TortoiseBaseUserAccountModel):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=150, null=True)
    status = fields.CharField(max_length=2, default=StatusOptions.Active.value)
    date_joined = fields.DatetimeField(default=timezone.now)
    updated_at = fields.DatetimeField(auto_now=True)

    # for typing
    contacts = fields.ReverseRelation["Contact"]

    class PydanticMeta:
        exclude = ["hashed_password"]

    def __str__(self):
        return f"{self.full_name}"
