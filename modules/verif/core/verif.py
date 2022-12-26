import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
from modules.verif import models

class Verif(commands.Cog):
    
    def __init__(self, client: commands.Bot):
        self.client = client

    async def cog_load(self):
        pass
        
    @app_commands.command()
    async def verif(self, interaction: discord.Interaction, member: discord.Member,name:str|None,age:int|None,how_find:str|None) -> None:
        await models.Verif.create(to_support_id=interaction.user.id,to_user_id=member.id,name=name,age=age,how_find=how_find)
        await interaction.response.send_message("got")

    
if __name__=="__main__":
    v = Verif(None)
    v.edit_img()
    
    # with Image.open("test.png") as im:
    #     draw = ImageDraw.Draw(im)
    
    #     xy = tuple([20,30])
        
    #     draw.multiline_text((10, 10), "Hello\nWorld", fill=(0, 0, 0))
    #     # draw.multiline_textbbox(xy=xy,text="FAHLFHEIUSHDKFJHCVCJB dsajf lkashdf ashkdf klasdj fhiaewu fhalskdj fasljd")
    #     # draw.line((0, 0) + im.size, fill=128)
    #     # draw.line((0, im.size[1], im.size[0], 0), fill=128)
        
    #     im.save("fsa.png")