import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from modules.verif import models

class Verif(commands.Cog):
    
    def __init__(self, client: commands.Bot):
        self.client = client

    async def cog_load(self):
        pass
        
    # TODO CHECK ADMIN
    @app_commands.command()
    async def verif(self, interaction: discord.Interaction, member: discord.Member,name:str|None,age:int|None,how_find:str|None) -> None:
        # if await self.__check_info(interaction,member,name,how_find):
        #     return
    
        model = await models.Verif.create(to_support_id=interaction.user.id,to_user_id=member.id,name=name,age=age,how_find=how_find)
        await self.estimate_support(model.pk, interaction.user,member)
        
        embed = discord.Embed(description=f' successful',color=0xafdafc)
        embed.set_author(name=f"{member} was verified ",icon_url=member.avatar)
        
        await interaction.response.send_message(embed=embed)
    
    # TODO CHECK ADMIN
    # todo Esli embed sliskom big
    @app_commands.command()
    async def verif_info(self, interaction: discord.Interaction, member: discord.Member) -> None:
        # ? not sure
        v_list = await models.Verif.filter(to_user_id=member.id)
    
        str_list = []
        for v in v_list:
            str_list.append(f"User id: {v.to_user_id}, Name:{v.name}, Age: {v.age}, How find: {v.how_find}, To_support_id: {v.to_support_id}, Support_rate: {v.support_rate}, Date: {v.date},  \n")
            
        embed = discord.Embed(description="".join(str_list),color=0xafdafc)
        embed.set_author(name=f' All verifications of {member}',icon_url=member.avatar)
        
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
    
    # async def __check_info(self, interaction: discord.Interaction,member:discord.Member,name: str, how_find:str) -> bool:
    #     if name != None and len(name) > 32:
    #             reason= "Len of 'name' is bigger then 32"
    #     if how_find != None and len(how_find) > 256:
    #         reason= "Len of 'how_find' is bigger then 32"
    #     else:
    #         return False
        
    #     embed = discord.Embed(description=f' not successful due to {reason}',color=0xafdafc)
    #     embed.set_author(name=f"{member} was verified ",icon_url=member.avatar)
        
    #     await interaction.response.send_message(embed=embed)
        
    #     return True