import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime
from security import is_admin_channel, is_in_channel, GetChannelByName, Error
import pygsheets
import pandas as pd
from googleapiclient import discovery
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os


def GetEmail(user):
    # File format should be username#1234 - email@gmail.com
    emails = open(os.path.join("files", "mod-emails.txt"), "r").readlines()
    for email in emails:
        if email.startswith(user):
            e = email.split(' - ')[1].strip()
            return e
    raise Error(
        "Your Gmail was not found, please contact the Bot's creator (David)")


def GetCredentials():
    """Read client_secret.json to gain permissions to access Google Sheets API"""
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
        'https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)

    client = gspread.authorize(credentials)
    return client


class Poll():
    def __init__(
        self,
        name,
        channel,
        options=[],
        key="",
        maxVotesPerOption=0,
        maxVotesPerPerson=1,
        creator="",
        create=False,
            adminLocked=False):
        self.name = name
        self.creator = GetEmail(creator)
        self.options = options
        self.channel = channel
        self.creator = GetEmail(creator)
        self.maxVotesPerOption = maxVotesPerOption
        self.maxVotesPerPerson = maxVotesPerPerson
        if create:
            self.sheet = self.ToGoogleSheet()
        else:
            self.sheet = self.Load(key)

    def GetSheet(self):
        if self.sheet is not None:
            return self.sheet
        else:
            self.Load(self.id)
            return self.sheet

    def Load(self, key):
        client = GetCredentials()
        self.sheet = client.open_by_key(key)
        self.id = key

    def ToGoogleSheet(self):
        client = GetCredentials()
        sheet = client.create(self.name)
        self.id = sheet.id
        self.SaveToFile()
        worksheet = sheet.get_worksheet(0)
        for x in range(1, len(self.options) + 1):
            worksheet.update_cell(x, 1, self.options[x - 1].strip())
        sheet.share(self.creator, perm_type='user', role='owner')
        return sheet

    def url(self):
        "It is easier to store just the id and generate the url dynamicly"
        return "https://docs.google.com/spreadsheets/d/%s" % self.id

    def SaveToFile(self):
        f = open("polls/" + self.channel + ".csv", "w")
        f.write(
            self.name +
            "," +
            self.id +
            "," +
            str(self.maxVotesPerOption) +
            "," +
            str(self.maxVotesPerPerson) +
            "," +
            ",".join(self.options)
        )
        f.close()

    def AddVote(self, choice, user):
        if len(choice) > 1:
            raise Error("Enter one letter as your vote.")
        choice = choice.upper()
        index = ord(choice) - 65
        if index < 0 or index > len(self.options):
            raise Error("Invalid option.")
        sheet = self.GetSheet().get_worksheet(0)
        matches = sheet.findall(user)
        if len(matches) >= self.maxVotesPerPerson and self.maxVotesPerPerson != 0:
            raise Error(
                "You've already voted the max amount of times. You may contact an admin to change your vote.")
        empty = True
        x = 1
        while empty:
            cell = sheet.cell(index + 1, x).value
            if cell == "":
                sheet.update_cell(index + 1, x, user)
                empty = False
            elif cell == user:
                raise Error(
                    "You already voted for that option. You may contact an admin to change your vote.")
            elif cell == "XXXXXX":
                raise Error("Sorry, that option is full")
            else:
                x = x + 1

    def Votes(self, index):
        """Returns a poll's votes for a given option index."""
        sheet = self.GetSheet().get_worksheet(0)
        row = sheet.row_values(index + 1)
        return row[1:]

    def AddOption(self, option):
        self.options.append(option)
        self.GetSheet().get_worksheet(0).update_cell(len(self.options), 1, option)
        self.SaveToFile()

    def SetVotesPerPerson(self, amnt):
        self.maxVotesPerPerson = amnt
        self.SaveToFile()


def GetPoll(channel):
    path = "polls/" + channel + ".csv"
    if not os.path.exists(path):
        raise Error("No poll in this channel")
    f = open(path, "r")
    details = f.read().split(',')
    f.close()
    name = details[0]
    key = details[1]
    maxPerOption = int(details[2])
    maxPerUser = int(details[3])
    poll = Poll(
        name=name,
        channel=channel,
        key=key,
        maxVotesPerPerson=maxPerUser)
    # TODO make it read from GSheet instead incase options change
    poll.options = details[4:]
    return poll


class Polls(commands.Cog):

    def __init__(self, settings, client):
        self.settings = settings
        self.client = client

    @commands.command(
        name="poll-new", help='Create a new poll. Format should be $poll-new channel "Poll name" "option1,option2,option3" ')
    @commands.check(is_admin_channel)
    async def CreatePoll(self, ctx, channel_name, name, *options):
        """Create a new poll."""
        channel = self.client.GetChannelByName(channel_name)
        choices = options[0].split(',')
        new_poll = Poll(
            channel=channel_name,
            name=name,
            options=choices,
            creator=str(ctx.message.author),
            create=True)
        await ctx.send("New poll created. It's been shared to your Gmail and you can view it at " + new_poll.url() + "\nChange a cell to XXXXXX to set the limit of votes for that option")

        channel_message = "New Poll: " + name + "\n"
        i = 'A'
        for option in choices:
            option = option.strip()
            channel_message = channel_message + \
                str(i) + ': ' + option + "\n"
            i = chr(ord(i[0]) + 1)
        channel_message = channel_message + "Vote with $vote choice"

        pins = await channel.pins()
        for pin in pins:
            if str(pin.author) == self.settings.bot:
                await pin.unpin()
                break
        pin_msg = await channel.sendBlock(channel_message)
        await pin_msg.pin()

    @commands.command(
        name="poll-option",
        help="Add a new option to the poll")
    @commands.check(is_admin_channel)
    async def AddOption(self, ctx, channel, option):
        poll = GetPoll(channel)
        poll.AddOption(option)
        await ctx.sendBlock("Added option")

    @commands.command(
        name="vote",
        help="Vote on the current channel's pole")
    async def Vote(self, ctx, choice):
        processing = await ctx.sendBlock("Processing your vote... These messages will be logged and deleted when completed...")
        user = str(ctx.message.author)
        channel = str(ctx.channel)
        poll = GetPoll(channel)
        poll.AddVote(choice, user)
        await processing.delete()
        await ctx.message.delete()
        await ctx.bot.GetChannelByName(ctx.bot.settings.poll_log).sendBlock(user + " voted for " + choice + " in " + channel)

    @commands.command(
        name="poll",
        help="Show info about the channel's current poll")
    async def PollInfo(self, ctx):
        channel = str(ctx.channel)
        poll = GetPoll(channel)
        i = 'A'
        msg = poll.name + "\n"
        for option in poll.options:
            i_int = ord(i[0]) - 65
            votes = str(len(poll.Votes(i_int)))
            msg = msg + str(i) + ": " + option.strip() + \
                "   Votes=" + votes + "\n"
            i = chr(ord(i[0]) + 1)
        msg = msg + "Vote with $vote choice"
        if await is_admin_channel(ctx):
            msg = msg + "\n" + poll.url()
        await ctx.sendBlock(msg)

    @commands.command(
        name="poll-vpp",
        help="Votes Per Person. Sets the amount of votes one person can make (Enter 0 for unlimited). Defaults to 1, does not change already made votes")
    @commands.check(is_admin_channel)
    async def SetVotesPerPerson(self, ctx, channel, amnt):
        poll = GetPoll(channel)
        poll.SetVotesPerPerson(int(amnt))
        if amnt == "0":
            amnt = "unlimited"
        await ctx.sendBlock("Changed votes per person to " + amnt)
