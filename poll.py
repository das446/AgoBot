import discord
import time
import asyncio
import csv
import sys
from discord.ext import commands
import configparser
from datetime import datetime
from security import is_admin_channel, is_in_channel, GetChannelByName
import pygsheets
import pandas as pd
from googleapiclient import discovery
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread


def GetCredentials():
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
        'https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)

    client = gspread.authorize(credentials)
    return client


class Poll():
    def __init__(
        self,
        name,
            channel,
        options,
        maxVotesPerOption=0,
        maxVotesPerPerson=0,
            create=False):
        self.name = name
        self.options = options
        self.channel = channel
        self.maxVotesPerOption = maxVotesPerOption
        self.maxVotesPerPerson = maxVotesPerPerson
        self.sheet = None
        if create:
                self.sheet = self.ToGoogleSheet()

        def GetSheet(self):
            if sheet is not None:
                return sheet
            else:

        def Load(self, key):
            client = GetCredentials()
            sheet = client.open_by_key(key)

    def ToGoogleSheet(self):
        client = GetCredentials()
        sheet = client.create(self.name)
        self.url = "https://docs.google.com/spreadsheets/d/%s" % sheet.id
        self.id = sheet.id
        self.SaveToFile()
        worksheet = sheet.get_worksheet(0)
        for x in range(1, len(self.options)):
            worksheet.update_cell(x, 1, self.options[x - 1])
        print(self.url)
        sheet.share('nintendavid26@aol.com', perm_type='user', role='owner')
        return sheet

    def SaveToFile(self):
        f = open("polls.csv", "a+")
        f.write(
            self.name +
            "," +
            self.url +
            "," +
            self.maxVotesPerOption +
            "," +
            self.maxVotesPerPerson +
            "\n")
        f.close()

    def MakeJsonRequest(self):
        body = {}
        body["properties"] = {"title": self.name}
        rows = [{"data": []}]
        i = 0
        body["sheets"] = rows
        for option in self.options:
            row = {"startRow": i, "rowData": [
                {"values": [{"userEnteredValue": {"stringValue": option}}]}]}
            rows.append(row)
            i = i + 1
        return json.dumps(body)

        def AddResponse():


class Polls(commands.Cog):

    def __init__(self, settings):
        self.settings = settings

    @commands.command(name="new", help="Create a new poll")
    @is_in_channel(["testground"])
    async def CreatePoll(ctx, channel, name, *options):
        channel = GetChannelByName(channel, self.settings)
        choices = options.split(',')
        new_poll = Poll(channel=channel, name=name, options=choices)
