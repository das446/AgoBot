import discord
from discord.ext import commands

class BoardGames(commands.Cog):

    def GetBetrayalGames(self):
        games=[]
        lines = open("betrayal-players.txt").readlines()
        for line in lines:
            line = line.strip() 
            
        return games


    @commands.command(name="betrayal", help="Shows info about Betrayal Legacy")
    async def Betrayal(self,ctx):
         await ctx.sendBlock(open(os.path.join("files","betrayal.txt")).read())

    @commands.command(name="betrayal-signup", help="Signup for a Betrayal Legacy game")
    async def Signup(self,ctx):
        user = ctx.message.author
        
