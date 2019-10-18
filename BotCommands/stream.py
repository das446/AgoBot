from twitch import TwitchClient
from discord.ext import commands


class Twitch(commands.Cog):
	@commands.command(pass_context=True, help="show info on the current stream")
	async def stream(self,ctx):
		print("cog")
