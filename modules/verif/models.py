from tortoise.models import Model
from tortoise import fields
from discord import Member

class Verif(Model):
    
    to_support = fields.ForeignKeyField("models.User",related_name="support_verifs")
    to_user = fields.ForeignKeyField("models.User",related_name="verifs")
    name = fields.CharField(max_length=32,null=True)
    age = fields.SmallIntField(null=True)
    how_find = fields.CharField(max_length=256,null=True)
    support_rate = fields.SmallIntField(default=None,null=True)
    date = fields.DatetimeField(auto_now_add=True)
    