import os
import requests
import pprint
import json
import time
from discord.ext import commands, tasks
from security import is_admin_channel, is_in_channel, Error


class Game:
    def __init__(self, game, status):
        self.game = game
        self.status = status
        self.game_type = "Video Games"
        if game == "Board Games":  #When streaming a board game the title should be "Game Name: Whatever you want"
            self.game_type = "Board Games"
            self.game = self.status.split(':')[0]

    def __str__(self):
        return self.game


async def OnLoop(bot, msg_channel=""):
    curGame = GetCurrentGame(bot.settings)
    prevGame = GetMostRecentGame(bot.settings)
    if prevGame != curGame.game:    
        lines = bot.settings.ReadFile("streams.txt").split("\n")
        lines.append(curGame.game.strip())
        bot.settings.WriteFile("streams.txt", "\n".join(lines))
        channel = bot.settings["channel_videogames"]
        if curGame.game_type == "Board Games":
            channel = bot.settings["channel_boardgames"]
        if msg_channel!="":
            channel = msg_channel
        msg = "We're streaming " + curGame.game
        print(msg)
        await bot.sendBlockToChannel(channel, msg)
        return curGame
    return curGame


def GetMostRecentGame(settings):
    lines = settings.ReadFile("streams.txt").split("\n")
    if len(lines) > 1:
        return lines[-1].strip()
    return ""


def GetCurrentGame(settings):
    channel = settings["twitch_id"]
    key = settings["twitch_key"]
    url = "https://api.twitch.tv/kraken/channels/" + channel
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': key
    }
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    game = Game(data["game"], data["status"])
    return game


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Loop.start()

    @tasks.loop(seconds=300)
    async def Loop(self):
        await OnLoop(self.bot)
    
    @Loop.before_loop
    async def pre_loop(self):
        await self.bot.wait_until_ready()

    @commands.command(
        name = "stream",
        help = "Show info about the current stream")
    async def StreamInfo(self, ctx):
        game = GetCurrentGame(ctx.bot.settings)
        await ctx.sendBlock("We're streaming "+str(game))    
    
    @commands.command(
        name="streams",
        help="Show a list of all the games we've streamed. (Since we started tracking them)")
    async def GameList(self, ctx):
        msg = "Here's the games we've played:\n"
        games = ctx.settings.ReadFile("streams.txt")
        print(games)
        await ctx.sendBlock(msg+games)
