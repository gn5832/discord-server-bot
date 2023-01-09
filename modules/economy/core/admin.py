import discord
from discord import app_commands
from discord.ext import commands
from modules.core.models import User
from modules.economy import models
from modules.configs.economy_config import *
from modules.core.admin import BaseAdmin

class EconomyAdmin(commands.Cog, BaseAdmin):
    def __init__(self, client: commands.Bot):
        self.client = client


    @app_commands.command()
    async def set_money(self, interaction: discord.Interaction, member: discord.Member, money: int):
        
        if money < 0: money = 0
        admin_user, created = await User.get_or_create_by_member(interaction.user)
        user, created = await User.get_or_create_by_member(member)
        if not self.is_owner_or_admin(admin_user, interaction.user):
            await interaction.response.send_message(embed=self.get_not_admin_error_embed())
            return

        await models.Economy.update_or_create(to_user=user, defaults=dict(balance=money))
        embed = discord.Embed(title=f'{member} теперь имеет на счету', description = f'```{money}{CURRENCY_ICON}```', color=0xafdafc)
        embed.set_author(name=f'{interaction.user} принудительно изменил баланс пользователя', icon_url=member.avatar)
        await interaction.response.send_message(embed=embed)
