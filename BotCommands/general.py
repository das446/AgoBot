import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime


class General(commands.Cog):

    @commands.command(name="stop", help='Stop the bot. (Admin only)')
    @commands.check(settings.is_admin_channel)
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


