import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime
from security import is_admin_channel, is_in_channel


class General(commands.Cog):

    @commands.command(name="stop", help='Stop the bot')
    @commands.check(is_admin_channel)
    async def Stop(self, ctx, *msg):
        channel = self.client.get_channel(self.settings.main_channel)
        if len(msg) > 0:
            await channel.sendBlock('AGO Bot will be down for maintenance')
        await self.client.logout()

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
            uptime = now - self.settings.start_time
            message = message + "Current Uptime: " + str(uptime)
            await ctx.sendBlock(message)

    @commands.command(name='schedule', help='Show weekly schedule')
    async def ShowSchedule(self, ctx):
        with open('schedule.txt') as schedule:
            await ctx.sendBlock(schedule.read())

    @commands.command(
        name='schedule-update',
        help='Update the schedule')
    @commands.check(is_admin_channel)
    async def UpdateSchedule(self, ctx, arg):
        channel = ctx.channel
        f = open("schedule.txt", "w+")
        f.write(arg)
        await ctx.sendBlock("Updated schedule")

        @commands.command(
            name="channel-ids",
            help="list the channel ids, which is needed for other commands")
        @commands.check(is_admin_channel)
        async def ChannelIds(ctx):
            s = self.settings.settings
            msg = ("general=" + s["channel_general"] + "\n" +
                   "anime=" + s["channel_anime"] + "\n" +
                   "rpg=" + s["channel_rpg"] + "\n" +
                   "videogames=" + s["channel_videogames"] + "\n" +
                   "boardgames=" + s["channel_boardgames"] + "\n" +
                   "cardgames=" + s["channel_cardgames"] + "\n" +
                   "cosplay=" + s["channel_cosplay"] + "\n")
            ctx.sendBlock(msg)

    def __init__(self, s, c):
        self.settings = s
        self.client = c
