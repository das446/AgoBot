import discord
from discord.ext import commands
from security import is_admin_channel, Error
import io 
import sys

class Emoji(commands.Cog):
    @commands.command(name="emoji-new",help= "Upload a new emoji") 
    @commands.check(is_admin_channel) 
    async def NewEmoji(self, ctx, name):
        if len(ctx.message.attachments)<=0:
            raise Error("You didn't upload an image")
        image = ctx.message.attachments[0]
        if not image.filename.lower().endswith(('.gif','.png','.jpg','jpeg')):
            raise Error("Not a valid file extension")
        guild = ctx.message.guild
        b = await image.read()
        if sys.getsizeof(b) > 256000:
            raise Error("The file must be smaller than 256 kB.")
       
        await guild.create_custom_emoji(name=name,image=b)
        await ctx.sendBlock("Uploaded emoji")
    
    commands.command(name="emoji-upload", help = "Uploads all of the emojis in a given folder")
    commands.check(is_admin_channel)
    async def BulkUploadEmojis(self, ctx):
        folder = os.path.join("files","emojis")
        guild = ctx.message.guild
        for f in os.listdir(folder):
            print(f)
            image = f.read()
            b = bytearray(image)
            await guild.create_custom_emoji(name=f.split('.')[0],image=b)

