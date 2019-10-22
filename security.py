from discord.ext import commands

dev = False


async def DevOnly(ctx):
    return dev


async def is_admin_channel(ctx):
    return str(ctx.channel) == "testground"


def is_in_channel(channels):
    async def predicate(ctx):
        return str(ctx.channel) in channels
    return commands.check(predicate)


def GetChannelByName(channel_name, settings):
    server = client.get_server(settings.server)
    for channel in server.channels:
        if channel.name == channel_name:
            return channel
