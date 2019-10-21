import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime
from BotCommands import general

client = commands.Bot(command_prefix='$bot ')

running = False


class Settings():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config')
        self.prod = 'prod'
        self.dev = 'dev'
        self.start_time = datetime.now()
        self.environment = dev
        if len(sys.argv) > 1:
            self.environment = sys.argv[1]

        self.settings = config[environment]

        self.main_channel = int(self.settings["channel_main"])
        self.admin_channel_name = self.settings["channel_admin_name"]

    async def is_admin_channel(ctx):
        return str(ctx.channel) == admin_channel_name


async def sendBlock(self, s):
    await self.send('```' + s + '```')

discord.channel.TextChannel.sendBlock = sendBlock
commands.context.Context.sendBlock = sendBlock


@client.event
async def on_ready():
    channel = client.get_channel(main_channel)
    print(type(channel))
    await channel.sendBlock("AGO Bot is operational.\nType $bot help to view available commands")


class General(commands.Cog):

    @commands.command(name="stop", help='Stop the bot. (Admin only)')
    @commands.check(is_admin_channel)
    async def Stop(self, ctx):
        print(type(ctx))
        channel = client.get_channel(main_channel)
        await channel.sendBlock('AGO Bot will be down for maintenance')
        await client.logout()

    @commands.command(name='events', help='Show upcoming events.')
    async def ShowEvents(self, ctx):
        with open('events.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            msg = ""
            for row in reader:
                msg = msg + ", ".join(row) + "\n\n"
            msg = 'Here are upcoming events:\n' + msg
            await ctx.sendBlock(msg)

    @commands.command(name='info', help='Show info about the bot')
    async def Info(self, ctx):
        with open('info.txt') as info:
            message = info.read()
            now = datetime.now()
            uptime = now - start_time
            message = message + "Current Uptime: " + str(uptime)
            await ctx.sendBlock(message)

    @commands.command(name='schedule', help='Show weekly schedule')
    async def ShowSchedule(self, ctx):
        with open('schedule.txt') as schedule:
            await ctx.sendBlock(schedule.read())

    @commands.command(
        name='schedule-update',
        help='Update the schedule, (Admins only, wrap it with double quotes)')
    @commands.check(is_admin_channel)
    async def UpdateSchedule(self, ctx, arg):
        channel = ctx.channel
        f = open("schedule.txt", "w+")
        f.write(arg)
        await ctx.sendBlock("Updated schedule")


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

settings = Settings()
g = general.general(settings)
g.settings=settings()

client.add_cog(general.General(settings))
# client.add_cog(BotCommands.stream.Twitch())
# client.add_cog(BotCommands.insta.Instagram())


if environment == prod:
    client.loop.create_task(loop())

client.run(settings['key'])
