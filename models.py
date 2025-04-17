from tortoise import fields
from tortoise.models import Model


class Article(Model):
    id = fields.BigIntField(pk=True, auto=True)
    title = fields.CharField(max_length=255, null=False)
    author = fields.CharField(max_length=255, null=True)
    description = fields.TextField(null=True)
    published_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "article"
        default_connection = "default"
