
from discord.ext import commands


class Instagram(commands.Cog):
	@commands.command(context=True, help="Posts our Instagram link")
	async	def link(self):
		print("instagram")
