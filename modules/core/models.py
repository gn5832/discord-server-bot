from tortoise.models import Model
from tortoise import fields
from discord import Member

class User(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(null=True, max_length=64)
    discriminator = fields.CharField(null=True, max_length=4)


    @classmethod
    async def get_or_create_by_member(cls, member: Member):
        return await cls.get_or_create(
            id=member.id,
            defaults=dict(
                name=member.name,
                discriminator=member.discriminator
            )
        )

    @classmethod
    async def update_or_create_by_member(cls, member: Member):
        return await cls.update_or_create(
            id=member.id,
            defaults=dict(
                name=member.name,
                discriminator=member.discriminator
            )
        )


    

    @property
    def full_name(self):
        if self.name and self.discriminator:
            return self.name + '#' + self.discriminator


    def __str__(self):
        return self.name


class Permissions(Model):
    to_user = fields.OneToOneField('models.User', related_name='permissions')
    is_admin = fields.BooleanField(default=False)
    is_curator = fields.BooleanField(default=False)
    is_moderator = fields.BooleanField(default=False)
    is_eventmod = fields.BooleanField(default=False)
    is_support = fields.BooleanField(default=False)


    @classmethod
    async def get_or_create_permissions(cls, user: User):
        permissions = await user.permissions
        if permissions:
            return permissions
        return await Permissions.create(to_user=user)

