import discord
from discord import Member
from discord.ext import commands
from discord import app_commands
from modules.economy import models
from modules.core.models import User
from modules.configs.economy_config import *
from modules.economy.core.admin import EconomyAdmin
from datetime import timedelta


class EconomyError(Exception): ...
class OnlyUserError(EconomyError): ...


class Economy(commands.Cog):


    def __init__(self, client: commands.Bot):
        self.client = client


    async def cog_load(self):
        await self.client.add_cog(EconomyAdmin(self.client))


    async def withdraw_money(self, member: Member, money: int):
        economy = await self.get_economy(member)
        if economy.balance < money:
            raise EconomyError(
                f'Для совершения операции, на счёте {member.mention} \
                должно быть минимум {money}{CURRENCY_ICON}, он имеет всего {economy.balance}{CURRENCY_ICON}'
                )
        economy.balance -= money

        await economy.save()
        return economy.balance


    async def deposit_money(self, member: Member, money: int):
        economy = await self.get_economy(member)
        economy.balance += money
        await economy.save()
        return economy.balance


    async def send_economy_error(
        self, 
        interaction: discord.Interaction, 
        title: int = 'Транзакция не прошла', 
        description: int = 'Неизвестная ошибка'
        ) -> None:

            embed = discord.Embed(
                title=title, 
                description = description, 
                color=0xafdafc
            )
            await interaction.response.send_message(embed=embed)

    
    async def raise_give_errors(self, interaction: discord.Interaction, member: discord.Member, money: int):
        if interaction.user == member:
            description=f'{interaction.user.mention} запрещено отправлять {CURRENCY_NAME} себе!'
        elif interaction.user.bot or member.bot:
            description=f'{interaction.user.mention} ты пытаешься перевести {CURRENCY_NAME} боту {member.mention}'
        elif money < MIN_GIVE_MONEY:
            description=f'{interaction.user.mention} минимальная сумма для перевода {MIN_GIVE_MONEY}{CURRENCY_ICON}'
        elif MAX_GIVE_MONEY and money > MAX_GIVE_MONEY:
            description=f'{interaction.user.mention} максимальная сумма для перевода {MIN_GIVE_MONEY}{CURRENCY_ICON}'
        else: 
            return
        raise EconomyError(description)


    @app_commands.command()
    async def give(self, interaction: discord.Interaction, member: discord.Member, money: int):
        await self.raise_give_errors(interaction, member, money)
        author_balance = await self.withdraw_money(interaction.user, money)
        member_balance = await self.deposit_money(member, money)
        embed = discord.Embed(
            title=f'Транзакция прошла успешно', 
            description = f'{interaction.user.mention} перевёл {money}{CURRENCY_ICON} на счёт {member.mention}', 
            color=0xafdafc
        )
        embed.add_field(name=f'Состояние счёта {interaction.user}', value=f'```{author_balance}{CURRENCY_ICON}```')
        embed.add_field(name=f'Состояние счёта {member}', value=f'```{member_balance}{CURRENCY_ICON}```')
        await interaction.response.send_message(embed=embed)

    @give.error
    async def on_give_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error.original, EconomyError):
            await self.send_economy_error(interaction, description=error.original)




    async def get_economy(self, member) -> models.Economy:
        user, created = await User.get_or_create_by_member(member)
        econony, created = await models.Economy.get_or_create(to_user=user)
        return econony

    async def get_balance(self, member):
        econony = await self.get_economy(member)
        return econony.balance


    @app_commands.command()
    async def balance(self, interaction: discord.Interaction, member: None|discord.Member) -> None:
        if not member or member.bot:
            member = interaction.user
        balance = await self.get_balance(member)
        embed = discord.Embed(description = f'```{balance}{CURRENCY_ICON}```', color=0xafdafc)
        embed.set_author(name=f'{member} имеет на счету', icon_url=member.avatar)
        embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed = embed)

    

    @app_commands.command()
    @app_commands.checks.cooldown(1, TIMELY_RATE_HOURS * 60 * 60, key=lambda i: (i.guild_id, i.user.id))
    async def timely(self, interaction: discord.Interaction) -> None:
        balance = await self.deposit_money(interaction.user, TIMELY_MONEY)
        embed = discord.Embed(
            title='Временная награда', 
            description = f'{interaction.user.mention}, вы получили {TIMELY_MONEY}{CURRENCY_ICON}\n\
                ```Всего на счету {balance}{CURRENCY_ICON}```', 
            color=0xafdafc)
        embed.set_thumbnail(url=interaction.user.avatar)
        embed.set_footer(text=f'Новая награда будет доступна через {TIMELY_RATE_HOURS}ч.')
        await interaction.response.send_message(embed = embed)

    @timely.error
    async def on_timely_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            print(error.retry_after)
            hours, minutes, seconds = str(timedelta(seconds=error.retry_after)).split(':')[:3]
            print(hours, minutes, seconds)
            seconds = seconds.split('.')[0]
            str_time = f'**{hours}**ч. **{minutes}**м. **{seconds}**с.'
            
            embed = discord.Embed(
            title='Временная награда', 
            description = f'{interaction.user.mention}, временная награда будет доступна через {str_time}', 
            color=0xafdafc)
            embed.set_thumbnail(url=interaction.user.avatar)
            await interaction.response.send_message(embed = embed)



