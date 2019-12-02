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
    fileName = os.path.join("files", "streams.txt")
    curGame = GetCurrentGame()
    prevGame = GetMostRecentGame(fileName).strip()
    if prevGame != curGame.game:
        open(fileName, "a+").write(curGame.game.strip() + "\n")
        channel = bot.settings["channel_videogames"]
        if curGame.game_type == "Board Games":
            channel = bot.settings["channel_boardgames"]
        if msg_channel!="":
            channel = msg_channel
        msg = "We're streaming " + curGame.game
        print(msg)
        await bot.sendBlockToChannel(channel, msg)
        return curGame
    return None


def GetMostRecentGame(f):
    lines = open(f, "r").readlines()
    if len(lines) > 1:
        return lines[-1].strip()
    return ""


def GetCurrentGame():
    channel = open(os.path.join("files", "twitch-id.txt")).read().strip()
    key = open(os.path.join("files", "twitch-key.txt")).read().strip()
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

    @tasks.loop(seconds=60)
    async def Loop(self):
        await OnLoop(self.bot)
    
    @Loop.before_loop
    async def pre_loop(self):
        await self.bot.wait_until_ready()

    @commands.command(
        name = "stream",
        help = "Show info about the current stream")
    async def StreamInfo(self, ctx):
        game = await OnLoop(ctx.bot,msg)
            
    @commands.command(
        name="streams",
        help="Show a list of all the games we've streamed. (Since we started tracking them)")
    async def GameList(self, ctx):
        msg = "Here's the games we've played:\n"
        fileName = os.path.join("files", "streams.txt")
        games = open(fileName, "r").readlines()
        await ctx.sendBlock(msg+"\n".join(games))
