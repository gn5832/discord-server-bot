import discord
from discord.ext import commands
from loguru import logger
from modules.core.models import User



class Core(commands.Cog):


    def __init__(self, client: commands.Bot):
        self.client = client


    async def cog_load(self):
        await self.update_or_create_all_guild_users()




    async def update_or_create_all_guild_users(self):
        '''При включение бота, все доступные юзеры добавляются/обновляются в базу.'''
        logger.info('Запущена синхронизация таблицы Users')
        all_members = self.client.guilds[0].members
        user_members = list(filter(lambda member: not member.bot, all_members))
        updated_counter, created_counter = 0, 0
        
        for member in user_members:
            user, created = await User.update_or_create_by_member(member)
            if created:
                created_counter += 1
            else:
                updated_counter += 1
        
        logger.success(f'Синхронизация таблицы User - created={created_counter}, updated={updated_counter}')


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        '''Все новые юзеры при входе на сервер сразу сохраняются в базу.'''
        user, created = await User.update_or_create_by_member(member)
        logger.debug(f'id={user.id}, name={user.full_name} зашёл на сервер - {created=}')






