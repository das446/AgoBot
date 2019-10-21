import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime
import general

client = commands.Bot(command_prefix='$')

running = False


async def sendBlock(self, s):
    await self.send('```' + s + '```')

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
        self.admin_channel_name = self.settings["channel_admin_name"]
        self.key = self.settings["key"]


settings = Settings()


@client.event
async def on_ready():
    channel = client.get_channel(settings.main_channel)
    print(type(channel))
    await channel.sendBlock("AGO Bot is operational.\nType $help to view available commands")


async def loop():
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

g = general.General(settings,client)

client.add_cog(g)
# client.add_cog(BotCommands.stream.Twitch())
# client.add_cog(BotCommands.insta.Instagram())


if settings.environment == settings.prod:
    client.loop.create_task(loop())

client.run(settings.key)
