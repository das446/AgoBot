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
from security import Error, GetChannelByName, ReadFile, WriteFile
import os
import twitch
import fb


client = commands.Bot(command_prefix='$')


async def sendBlock(self, s, mention=""):
    if mention != "":
        mention = "<@"+mention+">"
    return await self.send(mention + '```' + s + '```')


async def sendBlockToChannel(self, channel_name, msg):
    channel =  GetChannelByName(self,channel_name)
    return await channel.sendBlock(msg)


async def sendToChannel(self, channel_name, msg):
    channel = GetChannelByName(self,channel_name)
    return await channel.send(msg)


class Settings():
    def __init__(self):
        self.config = configparser.ConfigParser() 
        self.prod = 'prod'
        self.dev = 'dev'
        self.local = 'local'
        self.start_time = datetime.now() 
        self.environment = self.dev
        if len(sys.argv) > 1:
            self.environment = sys.argv[1]
        if self.environment == self.local or self.environment == "tux":
            aws = self.config.read('config')
            os.environ['AWS_ACCESS_KEY_ID']=self.config["dev"]["aws_key"]
            os.environ["AWS_SECRET_ACCESS_KEY"]=self.config["dev"]["aws_secret"]
        self.config.read_string(ReadFile('config').decode('ASCII'))

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
    
    def ReadFile(self, path, string=True):
        if self.environment == self.local:
            return open(os.path.join("files",path),"r").read()
        else:
            data = ReadFile(path)
            if string:
                return data.decode('ASCII')
            return data
    
    def WriteFile(self, path, data):
        if self.environment == "local":
            open(os.path.join(files,path),"w+").write(data)
        else:
            WriteFile(path, data)
    
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
        b = io.BytesIO()
        await attachment.save(b)
        client.settings.WriteFile(filename, b.getvalue().decode())
        await message.channel.sendBlock("Updated file " + filename)
    await client.process_commands(message)


@client.check
async def restrict_to_dev(ctx):
    """Allows a dev/local and production version of the bot to be running at the same time without interference"""
    if ctx.bot.settings.environment != "prod":
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
 
    elif type(error) == commands.errors.MissingRequiredArgument:
        await ctx.sendBlock("You're missing a required value in your command")
        return
    
    elif type(error) == commands.errors.CommandNotFound:
        return

    try:
        if error.original.handled:
            if error.original.file is not None:
                await ctx.sendBlock(str(error.original))
                await ctx.bot.GetChannelByName(ctx.bot.settings.bot_log).sendBlock(msg, mention = ctx.bot.settings["creator"],file=error.original.file)
                await ctx.bot.GetChannelByName(ctx.bot.settings.bot_log).sendBlock(str(error.original.file), mention = ctx.bot.settings["creator"])
            else:
                await ctx.sendBlock(str(error.original))
        else:
            await ctx.sendBlock("An unexpected error occured")
    except BaseException:
        try:
            stream = io.StringIO()
            traceback.print_tb(error.original.__traceback__, file=stream)
            error_msg = stream.getvalue()
            creator = ctx.bot.settings["creator"]
            await ctx.sendBlock("An error occured, please alert a server admin.")
            msg = str(type(error.original))+" "+str(error.original) + "\n" + str(error_msg)
            await ctx.bot.GetChannelByName(ctx.bot.settings.bot_log).sendBlock(msg, mention = ctx.bot.settings["creator"])
        
        except BaseException:
            stream = io.StringIO()
            traceback.print_tb(error.__traceback__, file=stream)
            error_msg = stream.getvalue()
            await ctx.sendBlock("An error occured, please alert a server admin.")

            msg = str(type(error))+" "+str(error) + "\n" + str(error_msg)
            await ctx.bot.GetChannelByName(ctx.bot.settings.bot_log).sendBlock(msg, mention = ctx.bot.settings["creator"])


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

    commands.context.Context.sendBlock = sendBlock
    running = False

    discord.channel.TextChannel.sendBlock = sendBlock
    commands.context.Context.sendBlock = sendBlock
    commands.context.Context.GetChannelByName = GetChannelByName
    commands.context.Context.sendBlockToChannel = sendBlockToChannel
    commands.context.Context.sendToChannel = sendToChannel

    client.add_cog(general.General())
    client.add_cog(fb.FaceBook(client))
    client.add_cog(poll.Polls())
    client.add_cog(find.Find())
    client.add_cog(twitch.Twitch(client))
    # client.add_cog(BotCommands.stream.Twitch())
    # client.add_cog(BotCommands.insta.Instagram())
    client.run(settings.key)
