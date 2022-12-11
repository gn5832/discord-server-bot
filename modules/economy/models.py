from tortoise.models import Model
from tortoise import fields

class Economy(Model):

    to_user = fields.OneToOneField('models.User', related_name='economy')
    balance = fields.BigIntField(default=0)

