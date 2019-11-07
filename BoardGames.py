import discord
from discord.ext import commands
import os
from security import is_admin_channel, is_in_channel, GetChannelByName, Error


class BoardGames(commands.Cog):

    def GetBetrayalGames(self, members):
        games = []
        game = None
        lines = open(
    os.path.join(
        "files",
        "betrayal-players.txt"),
         "r").readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("Game") and line.endwith(":"):
                games.append([])
                game = games[-1]
            elif line != "--------" and line != ""
                user = find(lambda u: u.name == line, members)
                game.append(user)
        return games

    def AddPlayer(self, games, game, user):
        for g in games:
            if user in g:
                raise Error("You're already signed up for a game.")
        if len(game) >= 5:
            raise Error("Sorry, that game is full.")
        game.append(user)
        return game

    def RemovePlayer(self, games, user):
        for game in games:
            if user in game:
                game.remove(user)
                return games
        raise Error("You aren't signed up for any games")

    def SaveGames(self, games):
        f = open(os.path.join("files", "betrayal-players.txt", "w"))
        i = 1
        for game in games:
            f.write("Game " + str(i) + ":")
            for player in game:
                f.write(str(player))
            i = i + 1

        f.close()

    @commands.command(
    name="random-boardgame",
     help="Help decide a boardgame to play")
    async def RandomBoardGame(self, ctx):
        games = open(os.path.join("files", "boardgames.txt")).readlines()
        game = random.choice(games).strip()
        await ctx.sendBlock("Try " + game)

    @commands.command(
    name="betrayal",
     help="Shows info about Betrayal Legacy.")
    async def Betrayal(self, ctx):
         await ctx.sendBlock(open(os.path.join("files", "betrayal.txt")).read())

    @commands.command(
    name="betrayal-signup",
     help="Signup for a Betrayal Legacy game. If you type $betrayal-signup")
    async def Signup(self, ctx, game_number):
        user = ctx.message.author
        members = ctx.channel.guild.members
        games = GetBetrayalGames(members)
        if game_number == "1":
            game = games[0]
            AddPlayer(games, game, user)
        elif game_number == "2":
            game = games[1]
            AddPlayer(games, game, user)
        elif game_number == "leave":
            games = RemovePlayer(games, user)

        SaveGames(games)
        await ctx.sendBlock("Thanks for signing up")

    @commands.command(name="betrayel-clear", help="Clears the currently signed up players."
    @commands.check(is_admin_channel)
    async def ClearBetrayal(self, ctx):
        games=[[], []]
        SaveGames(games)
        await ctx.send("Cleared all players")

    @commands.command(name="betrayal-remind", help="Send a DM to everyone signed up for the next Betrayal to remind them.")
    @commands.check(is_admin_channel)
        async def BetrayalRemind(self, ctx):
            games = GetBetrayalGames(self, ctx.channel.guild.members)
            for game in games:
                for player in game:
                    print(str(player))
