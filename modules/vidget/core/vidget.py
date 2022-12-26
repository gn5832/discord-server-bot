import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
# from modules.economy import models
# from modules.core.models import User


edit_config= {
    "Nickname":{
        "coords":(0,0),
        "text":"randomfasdfasd fasdf",
        # "fnt":fnt,
        "fil":(0,0,0)
    },
    "Comment":{
        "coords":(0,20),
        "text":"randomfasdfasd fasdf",
        # "fnt":fnt,
        "fil":(0,0,0)
    },
    "In_voice":{
        "coords":(0,40),
        "text":"randomfasdfasd fasdf",
        # "fnt":fnt,
        "fil":(0,0,0)
    },
    "In_channel":{
        "coords":(0,60),
        "text":"randomfasdfasd fasdf",
        # "fnt":fnt,
        "fil":(0,0,0)
    }
}

class Vidget(commands.Cog):
    temp = "test.png"
    img = "fsa.png"
    
    def __init__(self, client: commands.Bot):
        self.client = client

    async def cog_load(self):
        g = self.client.get_guild(1050969969313189918)
        b = g.banner
        b.read()
        
        b.save(self.temp)
        
        # g = self.client.get_guild(4133)
        
        
        
    @commands.Cog.listener() 
    async def on_message(self,message:discord.Message):
        pass    
    
    def edit_img(self):
        with Image.open(self.temp) as im:
            for item in edit_config.values():
                self.write_text(im,item["coords"],item["text"],item["fil"])
    
    def write_text(self,im:Image.Image,coords:tuple[float,float],text:str, fill:tuple[int,int,int]):
        draw = ImageDraw.Draw(im)
        draw.text(coords,text,fill=fill)
        # draw.text(coords,text,fill=fill,font=fnt)
        im.save(self.img)
    
if __name__=="__main__":
    v = Vidget(None)
    v.edit_img()
    
    # with Image.open("test.png") as im:
    #     draw = ImageDraw.Draw(im)
    
    #     xy = tuple([20,30])
        
    #     draw.multiline_text((10, 10), "Hello\nWorld", fill=(0, 0, 0))
    #     # draw.multiline_textbbox(xy=xy,text="FAHLFHEIUSHDKFJHCVCJB dsajf lkashdf ashkdf klasdj fhiaewu fhalskdj fasljd")
    #     # draw.line((0, 0) + im.size, fill=128)
    #     # draw.line((0, im.size[1], im.size[0], 0), fill=128)
        
    #     im.save("fsa.png")