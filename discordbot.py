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
import os
import twitch


client = commands.Bot(command_prefix='$')


async def sendBlock(self, s):
    return await self.send('```' + s + '```')


async def sendBlockToChannel(self, channel_name, msg):
    channel =  GetChannelByName(self,channel_name)
    return await channel.sendBlock(msg)


async def sendToChannel(self, channel_name, msg):
    channel = GetChannelByName(self,channel_name)
    return await channel.send(msg)


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

        self.main_channel = self.settings["channel_main"]
        self.admin_channel = self.settings["channel_admin"]
        self.poll_log = self.settings["poll_log"]
        self.bot_log = self.settings["bot_log"]
        self.server = self.settings["server"]
        self.key = self.settings["key"]
        self.bot = self.settings["bot_id"]
    def __getitem__(self, key):
        return self.settings[key]


@client.event
async def on_ready():
    """Called when the bot starts."""
    print("Bot started")
    if len(sys.argv) > 2:
        channel = client.GetChannelByName(settings.main_channel)
        await channel.sendBlock("AGO Bot is operational.\nType $help to view available commands")

# handle files
@client.event
async def on_message(message):
    """Used to update files that other commands read"""
    if message.author != client.user and message.channel == client.GetChannelByName(
            client.settings.admin_channel) and len(message.attachments) > 0:
        attachment = message.attachments[0]
        filename = attachment.filename
        if filename.endswith('.txt') or filename.endswith('csv'):
            await attachment.save(os.path.join("files", filename))
            await message.channel.sendBlock("Updated file " + filename)
    await client.process_commands(message)


@client.check
async def restrict_to_dev(ctx):
    """Allows a dev and production version of the bot to be running at the same time without interference"""
    if ctx.bot.settings.environment == "dev":
        return str(ctx.channel) == "testground"
    if ctx.bot.settings.environment == "prod":
        return str(ctx.channel) != "testground"


@client.event
async def on_command_error(ctx, error):
    """Displays a friendly error message to the user, and a detailed error message to mods if needed"""

    if type(error) == commands.errors.BadArgument:
        await ctx.sendBlock("One of your options isn't a number that needs to be.")
        return
    elif type(error) == commands.errors.CheckFailure:
        return

    try:
        if error.original.handled:
            await ctx.sendBlock(str(error.original))
        else:
            await ctx.sendBlock("An unexpected error occured")
    except BaseException:
        try:
            stream = io.StringIO()
            traceback.print_tb(error.original.__traceback__, file=stream)
            error_msg = stream.getvalue()
            await ctx.sendBlock("An error occured, please alert a server admin.")
            await ctx.bot.GetChannelByName(ctx.bot.settings.bot_log).sendBlock(str(type(error.original)) + " " + str(error.original) + "\n" + str(error_msg))
        except BaseException:
            stream = io.StringIO()
            traceback.print_tb(error.__traceback__, file=stream)
            error_msg = stream.getvalue()
            await ctx.sendBlock("An error occured, please alert a server admin.")
            await ctx.bot.GetChannelByName(ctx.bot.settings.bot_log).sendBlock(str(type(error)) + " " + str(error) + "\n" + str(error_msg))


async def loop(self):
    """Polls FaceBook and other sources"""
    running = True
    await client.wait_until_ready()
    channel = client.get_channel(test_channel)
    while running:
        await asyncio.sleep(60)
        # fb.OnLoop(self)
        twitch.OnLoop(self)


def main():
    print("Program started")
    global client
    settings = Settings()
    client.settings = settings

    commands.Bot.GetChannelByName = GetChannelByName
    commands.Bot.sendBlockToChannel = sendBlockToChannel

    running = False

    discord.channel.TextChannel.sendBlock = sendBlock
    commands.context.Context.sendBlock = sendBlock
    commands.context.Context.GetChannelByName = GetChannelByName
    commands.context.Context.sendBlockToChannel = sendBlockToChannel
    commands.context.Context.sendToChannel = sendToChannel

    client.add_cog(general.General())
    client.add_cog(poll.Polls())
    client.add_cog(find.Find())
    client.add_cog(twitch.Twitch(client))
    # client.add_cog(BotCommands.stream.Twitch())
    # client.add_cog(BotCommands.insta.Instagram())
    client.run(settings.key)
