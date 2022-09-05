from tortoise import fields, models


class BaseModel(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return self.pk

    class Meta:
        abstract = True


class LabelMixin:
    label = fields.CharField(max_length=15)
