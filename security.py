from discord.ext import commands

dev = False


class Error(Exception):
    """This is a custom error message class that can be created and raised to immediately stop a 
       function's execution in a friendly manner. 
       See discordbot.on_command_error
    """
    def __init__(self, message):
        self.message = message
        self.handled = True


async def is_admin_channel(ctx):
    """Returns whether the context's channel is an admin channel"""
    return str(ctx.channel) in ["testground", "mods-are-gods"]


def is_in_channel(channels):
    async def predicate(ctx):
        return str(ctx.channel) in channels
    return commands.check(predicate)

# self=client


def GetChannelByName(self, channel_name):
    channels = self.get_all_channels()
    for channel in channels:
        if str(channel.name) == channel_name and str(channel.type) == "text":
            return channel
    raise Error("No channel named " + channel_name)
