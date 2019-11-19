import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime
from security import is_admin_channel, is_in_channel
import os
import random


class General(commands.Cog):

    @commands.command(name="stop", help='Stop the bot')
    @commands.check(is_admin_channel)
    async def Stop(self, ctx, *msg):
        """Stops the bot,"""
        channel = self.client.get_channel(self.settings.main_channel)
        if len(msg) > 0:
            await channel.sendBlock('AGO Bot will be down for maintenance')
        await self.client.logout()

    @commands.command(name='events', help='Show upcoming events.')
    async def ShowEvents(self, ctx):
        """Shows upcoming events by reading files/events.txt"""
        with open(os.path.join('files', 'events.txt'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            msg = ""
            for row in reader:
                msg = msg + ", ".join(row) + "\n\n"
            msg = 'Here are upcoming events:\n' + msg
            await ctx.sendBlock(msg)

    @commands.command(name='info', help='Show info about the bot')
    async def Info(self, ctx):
        """Shows info about the bot by reading files/info.txt"""
        with open(os.path.join('files', 'info.txt')) as info:
            message = info.read()
            now = datetime.now()
            uptime = now - self.settings.start_time
            message = message + "Current Uptime: " + str(uptime)
            await ctx.sendBlock(message)

    @commands.command(name='schedule', help='Show weekly schedule')
    async def ShowSchedule(self, ctx):
        """Shows the weekly schedule by reading files/schedule.txt"""
        with open(os.path.join("files", 'schedule.txt')) as schedule:
            await ctx.sendBlock(schedule.read())

    def __init__(self, s, c):
        self.settings = s
        self.client = c

    @commands.command(name="playing", help="Set the bot's activity status")
    @commands.check(is_admin_channel)
    async def SetPlaying(self, ctx, game_name):
        game = discord.Game(name=game_name)
        await self.client.change_presence(status=discord.Status.online, activity=game)
        await ctx.sendBlock("Set status to " + game_name)

    @commands.command(name="random-boardgame",
                      help="Help decide a boardgame to play")
    async def RandomBoardGame(self, ctx):
        games = open(os.path.join("files", "boardgames")).readlines()
        game = random.choice(games).strip()
        await ctx.sendBlock("Try " + game)
