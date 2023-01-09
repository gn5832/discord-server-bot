from modules.core.models import User, Permissions
from discord import Member, Embed
from discord.ext import commands
import discord
from discord import app_commands
from discord.ext import commands
from tortoise.expressions import Q


class BaseAdmin:

    def is_owner(self, member: Member):
        if self.client.guilds[0].owner == member:
            return True
        return False

    

    async def is_admin(self, user: User):
        permissions = await Permissions.get_or_create_permissions(user)

        if permissions.is_admin:
            return True
        return False

    async def is_owner_or_admin(self, user: User, member: Member):
        if self.is_owner(member) or await self.is_admin(user):
            return True
        return False


    def get_not_admin_error_embed(self):
        return Embed(
            title=f'Эта команда доступна только администраторам.', 
            description = f'Для получения доступа к ней, обратись к {self.client.guilds[0].owner.mention}', color=0xafdafc
            )
    def get_not_owner_error_embed(self):
        return Embed(
            title=f'Эта команда доступна только владельцу сервера.', 
            description = f'Для получения доступа к ней, обратись к {self.client.guilds[0].owner.mention}', color=0xafdafc
            )



class CoreAdmin(commands.Cog, BaseAdmin):
    def __init__(self, client: commands.Bot):
        self.client = client

    




    @app_commands.command()
    async def add_admin(self, interaction: discord.Interaction, member: discord.Member):

        if member.bot:
            await interaction.response.send_message(f'```Невозможно назначить бота администратором!```', delete_after=15)
            return

        admin_user, created = await User.get_or_create_by_member(interaction.user)
        user, created = await User.get_or_create_by_member(member)

        if not await self.is_owner_or_admin(admin_user, interaction.user):
            await interaction.response.send_message(embed=self.get_not_admin_error_embed())
            return
        if user.is_admin:
            await interaction.response.send_message(f'```Операция невозможна, {member} уже является администратором!```', delete_after=15)
            return

        permissions = await Permissions.get_or_create_permissions(user)
        permissions.is_admin = True
        await permissions.save()
        embed = Embed(
            title='Назначен новый администратор!',
            description=f'{interaction.user.mention} назначил администратором {member.mention}'
            )
        await interaction.response.send_message(embed=embed)


    @app_commands.command()
    async def remove_admin(self, interaction: discord.Interaction, member: discord.Member):

        if member.bot:
            await interaction.response.send_message(f'Невозможно лишить бота прав администратора, ими могут быть только люди!', delete_after=15)
            return

        admin_user, created = await User.get_or_create_by_member(interaction.user)
        user, created = await User.get_or_create_by_member(member)

        if not self.is_owner(interaction.user):
            await interaction.response.send_message(embed=self.get_not_owner_error_embed())
            return
        permissions = await Permissions.get_or_create_permissions(user)

        if not permissions.is_admin:
            await interaction.response.send_message(f'```Операция невозможна, {member} уже не имеет прав администратора!```', delete_after=15)
            return
        
        permissions.is_admin = True
        await permissions.save()

        embed = Embed(
            title='Администратор разжалован владельцем сервера!',
            description=f'{interaction.user.mention} снял права администратора с {member.mention}'
            )
        await interaction.response.send_message(embed=embed)
        

        
        
        
