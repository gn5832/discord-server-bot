import os
import json
import discord
from loguru import logger
from modules.economy.core.economy import Economy
from discord.ext import commands
from modules.core import orm
from modules.core.core import Core



class Client(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(intents=intents, command_prefix='!')

    async def on_ready(self):
        user = str(self.user)
        id = self.user.id
        logger.success(f'Бот успешно запущен. {user=} {id=}')
        await orm.init()
        await self.add_cogs()
        await self.sync_cogs()
        


    async def add_cogs(self):
        await self.add_cog(Core(self))
        await self.add_cog(Economy(self))


    async def sync_cogs(self):
        try:
            synced = await self.tree.sync()
            logger.info(f'Synced {len(synced)} commands')
        except Exception as ex:
            print(ex)


    async def on_voice_state_update(self, member, before, after):
        print(member, ' iii')


    @staticmethod
    def get_token():
        with open(os.path.join('modules', 'configs', 'TOKEN.json') ) as f:
            return json.load(f) 

