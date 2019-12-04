import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime
from security import is_admin_channel, is_in_channel, Error
import os
import random
import typing
import qrcode

class General(commands.Cog):

    @commands.command(name="test-mention")
    @commands.check(is_admin_channel)
    async def Mention(self, ctx):
        await ctx.sendBlock("test",mention = ctx.bot.settings["creator"])

    @commands.command(name="stop", help='Stop the bot')
    @commands.check(is_admin_channel)
    async def Stop(self, ctx, *msg):
        """Stops the bot,"""
        channel = ctx.bot.get_channel(ctx.bot.settings.main_channel)
        if len(msg) > 0:
            await channel.sendBlock('AGO Bot will be down for maintenance')
        await ctx.bot.logout()

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
            uptime = now - ctx.bot.settings.start_time
            message = message + "Current Uptime: " + str(uptime)
            await ctx.sendBlock(message)

    @commands.command(name='schedule', help='Show weekly schedule')
    async def ShowSchedule(self, ctx):
        """Shows the weekly schedule by reading files/schedule.txt"""
        with open(os.path.join("files", 'schedule.txt')) as schedule:
            await ctx.sendBlock(schedule.read())

    @commands.command(name="playing", help="Set the bot's activity status")
    @commands.check(is_admin_channel)
    async def SetPlaying(self, ctx, game_name):
        game = discord.Game(name=game_name)
        await ctx.bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.sendBlock("Set status to " + game_name)

    @commands.command(
        name="boardgame",
        help="Help decide a boardgame to play. Type a number to list that many games, and/or a letter or word to filter by it's title.")
    async def RandomBoardGame(self, ctx, amount: typing.Optional[int] = 1, title_filter=""):
        if amount < 1:
            raise Error("Enter a positive number for amount")
        games = open(os.path.join("files", "boardgames.txt")).readlines()
        if len(title_filter) == 1:
            games = filter(lambda g: g.startswith(title_filter), games)
        elif len(title_filter) > 1:
            games = filter(lambda g: title_filter.lower() in g.lower(), games)
        games = list(games)
        if len(games) == 0:
            raise Error("No games found.")
        random.shuffle(games)
        chosen_games = games[:amount]
        await ctx.sendBlock("Try:\n" + "".join(chosen_games))

    @commands.command(name = "qr", help = "Generate a qr code. Can be posted in chat or DM'ed")
    async def MakeQr(self, ctx, text, dm="False"):
        img = qrcode.make(text)
        img_path = os.path.join("files","qr.png")
        img.save(img_path,"PNG")
        if dm != "False":
            await ctx.author.send(text, file = discord.File(img_path))
        else:
            await ctx.send(text, file = discord.File(img_path))
        
