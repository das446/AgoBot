import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime
import general
import poll
import find
import traceback
import io
from security import Error, GetChannelByName

print("Program started")

client = commands.Bot(command_prefix='$')

commands.Bot.GetChannelByName = GetChannelByName

running = False


async def sendBlock(self, s):
    return await self.send('```' + s + '```')

discord.channel.TextChannel.sendBlock = sendBlock
commands.context.Context.sendBlock = sendBlock


class Settings():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config')
        self.prod = 'prod'
        self.dev = 'dev'
        self.start_time = datetime.now()
        self.environment = self.dev
        if len(sys.argv) > 1:
            self.environment = sys.argv[1]

        self.settings = self.config[self.environment]

        self.main_channel = int(self.settings["channel_main"])
        self.admin_channel = int(self.settings["channel_admin"])
        self.admin_channel_name = self.settings["channel_admin_name"]
        self.server = self.settings["server"]
        self.key = self.settings["key"]
        self.bot = self.settings["bot_id"]


settings = Settings()


@client.event
async def on_ready():
    """Called when the bot starts."""
    print("Bot started")
    if len(sys.argv) > 2:
        channel = client.get_channel(settings.main_channel)
        await channel.sendBlock("AGO Bot is operational.\nType $help to view available commands")

# handle files
@client.event
async def on_message(message):
    """Used to update files that other commands read"""
    if message.author != client.user and str(
            message.channel) == settings.admin_channel_name and len(
            message.attachments) > 0:
        attachment = message.attachments[0]
        filename = attachment.filename
        if filename.endswith('.txt'):
            await attachment.save(os.path.join("files", filename))
            await message.channel.sendBlock("Updated file " + filename)
    await client.process_commands(message)


@client.check
async def restrict_to_dev(ctx):
    """Allows a dev and production version of the bot to be running at the same time without interference"""
    if settings.environment == "dev":
        return str(ctx.channel) == "testground"
    if settings.environment == "prod":
        return str(ctx.channel) != "testground"


@client.event
async def on_command_error(ctx, error):
    """Displays a friendly error message to the user, and a detailed error message to mods if needed"""
    if hasattr(error.original, 'handled'):
        await ctx.sendBlock(str(error.original))
    else:
        stream = io.StringIO()
        traceback.print_tb(error.original.__traceback__, file=stream)
        error_msg = stream.getvalue()
        await ctx.sendBlock("An error occured, please alert a server admin.")
        await client.get_channel(settings.admin_channel).sendBlock(str(error) + "\n" + str(error_msg))


async def loop():
    """Polls FaceBook and other sources"""
    running = True
    await client.wait_until_ready()
    channel = client.get_channel(test_channel)
    while running:
        await asyncio.sleep(60)
        post = fb.GetMostRecentPost()
        if post != last_post:
            channels = post.getChannels()
            for channel in channels:
                channel.send(post)

g = general.General(settings, client)

client.add_cog(g)
client.add_cog(poll.Polls(settings, client))
client.add_cog(find.Find(client))
# client.add_cog(BotCommands.stream.Twitch())
# client.add_cog(BotCommands.insta.Instagram())

# if settings.environment == settings.prod:
#    client.loop.create_task(loop())

client.run(settings.key)
