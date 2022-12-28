import discord
from tortoise.exceptions import ValidationError
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from modules.verif import models
from modules.core.models import User

class Verif(commands.Cog):
    
    def __init__(self, client: commands.Bot):
        self.client = client

    async def cog_load(self):
        pass
        
    @app_commands.command()
    async def verif(self, interaction: discord.Interaction, member: discord.Member,name:str|None,age:int|None,how_find:str|None) -> None:
        # if await self.__is__avaible(interaction.user.id)== False:
        #     return
    
        model = await models.Verif.create(to_support_id=interaction.user.id,to_user_id=member.id,name=name,age=age,how_find=how_find)
        await self.estimate_support(model.pk, interaction.user,member)
        
        embed = discord.Embed(description=f' successful',color=0xafdafc)
        embed.set_author(name=f"{member} was verified ",icon_url=member.avatar)
        
        await interaction.response.send_message(embed=embed)
    
    # todo Esli embed sliskom big
    @app_commands.command()
    async def verif_info(self, interaction: discord.Interaction, member: discord.Member) -> None:
        # if await self.__is__avaible(interaction.user.id)== False:
        #     return
        v_list = await models.Verif.filter(to_user_id=member.id)
    
        str_list = []
        for v in v_list:
            str_list.append(f"User id: {v.to_user_id}, Name:{v.name}, Age: {v.age}, How find: {v.how_find}, To_support_id: {v.to_support_id}, Support_rate: {v.support_rate}, Date: {v.date},  \n")
            
        embed = discord.Embed(description="".join(str_list),color=0xafdafc)
        embed.set_author(name=f' All verifications of {member}',icon_url=member.avatar)
        
        await interaction.response.send_message(embed=embed)
        
    @verif.error
    async def on_verif_error(self, interaction: discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error.original,ValidationError):
            embed = discord.Embed(description="The len of name > 32 or the len of how_find > 256",color=0xafdafc)
            embed.set_author(name=f'Error ',icon_url=interaction.user.avatar)
        
            await interaction.response.send_message(embed=embed)
        
    async def estimate_support(self,id: models.Verif.pk, support: discord.User, member: discord.Member) -> None:
        embed = discord.Embed(description="Estimate your support",color=0xafdafc)
        embed.set_author(name=f'Your support {support}', icon_url=support.avatar)
        
        v = View()
        
        for i in range(5):
            button = Button(custom_id=str(i+1)+str(member.id),label=str(i+1))
            button.callback = await self.__btn_callback(i+1,id=id)
            v.add_item(button)
        
        await member.send(embed=embed,view=v)        
    
    async def __btn_callback(self, rate:int,id:models.Verif.pk):
        async def __callback(interaction: discord.Interaction):
            embed = discord.Embed(description="Thanks for estimatinf",color=0xafdafc)
            await interaction.response.edit_message(embed=embed,view=View())
            await models.Verif.filter(id=id).update(support_rate=rate)
        return __callback
    
    @staticmethod
    async def __is__avaible(id:int)->bool:
        u = await User.filter(id=id)
        if  u[0].is_admin == False and u[0].is_moderator == False and u[0].is_support == False:
            return False
        return True
    
    