from discord.ext import commands

dev = False


class Error(Exception):
    def __init__(self, message):
        self.message = "Handled: "+message
        self.handled = True


async def DevOnly(ctx):
    return dev


async def is_admin_channel(ctx):
    return str(ctx.channel) in ["testground", "mods-are-gods"]


def is_in_channel(channels):
    async def predicate(ctx):
        return str(ctx.channel) in channels
    return commands.check(predicate)


def GetChannelByName(channel_name, settings, client):
    channels = client.get_all_channels()
    for channel in channels:
        if str(channel.name) == channel_name and str(channel.type) == "text":
            return channel
    raise Error("No channel named " + channel_name)
