import discord
from discord.ext import commands


class Find(commands.Cog):
    @commands.command(name="find", help="Find text in past messages")
    async def Find(self, ctx, text):
        msg = await ctx.send("Searching...")
        text = text.lower()
        server = ctx.message.channel.guild
        urls = []
        for channel in server.channels:
            if str(channel.type) == 'text':
                try:
                    for message in await channel.history(limit=500).flatten():
                        m = message.content.lower()
                        if text in m and not m.startswith("$find"):
                            urls.append(message.jump_url)
                except BaseException:
                    print("Couldn't read channel " + str(channel))
        text = "Found these messages:\n"+"\n".join(urls)
        await msg.edit(content=text[0:2000])
