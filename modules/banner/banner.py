from discord.ext import commands
from loguru import logger
import asyncio
from modules.configs.banner_config import *
from modules.banner.make_banner import*





class Banner(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.guild = self.client.guilds[0]
        self.before_in_voice_members_len = 0


        if BANNER_TYPE == 'gif':
            self.banner_creator = GifBanner
        else:
            self.banner_creator = PngBanner


    async def cog_load(self):
        await self.banner_loop()


    def get_in_voice_members_len(self):
        return len(self.guild._voice_states)
        

    async def banner_loop(self):
        while True:
            await asyncio.sleep(REFRESH_TIME)
            in_voice_members_len = self.get_in_voice_members_len() + CHEAT_IN_VOICE_COUNTER
            if in_voice_members_len == self.before_in_voice_members_len:
                logger.debug(f'pass banner update')
                continue
            banner = self.banner_creator().make(in_voice_members_len)
            await self.guild.edit(banner=banner)
            logger.debug(f'banner updated')
            self.before_in_voice_members_len = in_voice_members_len



