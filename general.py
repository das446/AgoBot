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
import io
import socket

class General(commands.Cog):

    @commands.command(name="where")
    @commands.check(is_admin_channel)
    async def Where(self, ctx):
        await ctx.sendBlock(str(socket.gethostname()))

    @commands.command(name="env")
    @commands.check(is_admin_channel)
    async def Env(self, ctx):
        await ctx.sendBlock(ctx.bot.settings.environment)

    @commands.command(name="stop", help='Stop the bot')
    @commands.check(is_admin_channel)
    async def Stop(self, ctx, *msg):
        """Stops the bot"""
        channel = ctx.bot.get_channel(ctx.bot.settings.main_channel)
        if len(msg) > 0:
            await channel.sendBlock('AGO Bot will be down for maintenance')
        await ctx.bot.logout()

    @commands.command(name='info', help='Show info about the bot')
    async def Info(self, ctx):
        """Shows info about the bot by reading files/info.txt"""
        info = ctx.bot.settings.ReadFile('info.txt')
        message = info
        now = datetime.now()
        uptime = now - ctx.bot.settings.start_time
        message = message + "Current Uptime: " + str(uptime)
        await ctx.sendBlock(message)

    @commands.command(name='schedule', help='Show weekly schedule')
    async def ShowSchedule(self, ctx):
        """Shows the weekly schedule by reading files/schedule.txt"""
        schedule = ctx.bot.settings.ReadFile('schedule.txt')
        await ctx.sendBlock(schedule)

    @commands.command(name="playing", help="Set the bot's activity status")
    @commands.check(is_admin_channel)
    async def SetPlaying(self, ctx, game_name):
        game = discord.Game(name=game_name)
        await ctx.bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.sendBlock("Set status to " + game_name)

    @commands.command(name = "qr", help = "Generate a qr code. Can be posted in chat or DM'ed")
    async def MakeQr(self, ctx, text, dm="False"):
        #TODO: Make image exist only as bytes in memory
        img = qrcode.make(text)
        filename = 'qr'+str(random.randint(1,10000000))+'.png'
        img.save(filename,'PNG')
        if dm != "False":
            await ctx.author.send(text, file = discord.File(filename))
        else:
            await ctx.send(text, file = discord.File(filename))
        os.remove(filename)
