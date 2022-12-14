import discord
from discord.ext import commands
from discord import app_commands
from modules.economy import models
from modules.core.models import User

class EconomyError(Exception): ...
class OnlyUserError(EconomyError): ...


class Economy(commands.Cog):


    def __init__(self, client: commands.Bot):
        self.client = client

    async def withdraw_money(self, member, money):
        # implementation here
        ...

    async def deposit_money(self, member, money):
        # implementation here
        ...


    async def get_economy(self, member) -> models.Economy:
        user, created = await User.get_or_create_by_member(member)
        econony, created = await models.Economy.get_or_create(to_user=user)
        return econony

    async def get_balance(self, member):
        econony = await self.get_economy(member)
        return econony.balance

    @app_commands.command()
    async def set_money(self, interaction: discord.Interaction, member: discord.Member, money: int):
        if money < 0: money = 0
        user, created = await User.get_or_create_by_member(member)
        await models.Economy.update_or_create(to_user=user, defaults=dict(balance=money))
        embed = discord.Embed(title=f'{member} имеет на счету', description = f'```{money} монет```', color=0xafdafc)
        embed.set_author(name=f'{interaction.user} принудительно изменил баланс пользователя', icon_url=member.avatar)
        await interaction.response.send_message(embed = embed)





    @app_commands.command()
    async def balance(self, interaction: discord.Interaction, member: None|discord.Member) -> None:
        if not member or member.bot:
            member = interaction.user
        balance = await self.get_balance(member)
        embed = discord.Embed(description = f'```{balance} монет```', color=0xafdafc)
        embed.set_author(name=f'{member} теперь имеет на счету', icon_url=member.avatar)
        await interaction.response.send_message(embed = embed)





    # @commands.Cog.listener()
    # async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
    #     print(interaction, error)