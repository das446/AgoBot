import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime
import BotCommands
import fb


config = configparser.ConfigParser()
config.read('config')

prod = 'prod'
dev = 'dev'

start_time = datetime.now()

environment = dev
if len(sys.argv)>1:
	environment = sys.argv[1]

client = commands.Bot(command_prefix='$bot ')

test_channel = 628989969708351509
general_channel = 533351899798306818

running = False

def ToBlock(s):
	return('```'+s+'```')

@client.event
async def on_ready():
		channel = client.get_channel(test_channel)
		if environment == prod:
			channel = client.get_channel(general_channel)
		await channel.send(ToBlock("AGO Bot is operational.\nType $bot help to view available commands"))	


class General(commands.Cog):

	@commands.command(name="stop", help='Stop the bot. (Admin only)')
	async def Stop(self, ctx):
		channel = ctx.channel		
		if str(channel) == 'testground':
			if environment==prod:
				channel = client.get_channel(general_channel)
			else:
				channel = client.get_channel(test_channel)
			await channel.send(ToBlock('AGO Bot will be down for maintenance'))
			await client.logout()

	@commands.command(name='events', help='Show upcoming events.')
	async def ShowEvents(self,ctx):
		with open('events.csv',newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter='|')
			msg = ""
			for row in reader:
				msg = msg + ", ".join(row)+"\n\n"
			msg = 'Here are upcoming events:\n'+msg
			await ctx.send(ToBlock(msg))

	@commands.command(name='info', help='Show info about the bot')
	async def Info(self,ctx):
		with open('info.txt') as info:
			message = info.read()
			now = datetime.now()
			uptime = now - start_time
			message = message+"Current Uptime: "+str(uptime)
			await ctx.send(ToBlock(message))

	@commands.command(name='schedule', help='Show weekly schedule')
	async def ShowSchedule(self,ctx):
		with open('schedule.txt') as schedule:
			await ctx.send(ToBlock(schedule.read()))

	@commands.command(name='schedule-update',help='Update the schedule, (Admins only, wrap it with double quotes)')
	async def UpdateSchedule(self,ctx, arg):
		channel = ctx.channel
		if str(channel) == 'testground':
			f = open("schedule.txt","w+")
			f.write(arg)
			await ctx.send(ToBlock("Updated schedule"))


async def loop():
	running = True
	await client.wait_until_ready()
	channel = client.get_channel(test_channel)
	while running:
		await asyncio.sleep(60)
		post = fb.GetMostRecentPost()
		channels = post.getChannels()
		for channel in channels:
			channel.send(post)

client.add_cog(General())
#client.add_cog(BotCommands.stream.Twitch())
#client.add_cog(BotCommands.insta.Instagram())


if environment == prod:
	client.loop.create_task(loop())

client.run(config['Default']['key'])
