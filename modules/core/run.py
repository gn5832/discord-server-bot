import os
import json
import discord
from loguru import logger
from modules.economy.core.economy import Economy
from discord.ext import commands
from modules.core import orm
from modules.core.core import Core

from discord import utils
import asyncio
from tortoise import Tortoise



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

    def run(
        self,
        token: str,
        *,
        reconnect: bool = True,
        log_handler = utils.MISSING,
        log_formatter = utils.MISSING,
        log_level: int = utils.MISSING,
        root_logger: bool = False,
    ) -> None:

        async def runner():
            async with self:
                await self.start(token, reconnect=reconnect)

        if log_handler is not None:
            utils.setup_logging(
                handler=log_handler,
                formatter=log_formatter,
                level=log_level,
                root=root_logger,
            )

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            # nothing to do here
            # `asyncio.run` handles the loop cleanup
            # and `self.start` closes all sockets and the HTTPClient instance.
            asyncio.run(Tortoise.close_connections())


    
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

