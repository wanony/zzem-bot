# import discord
from discord.ext import commands
import json
with open('directories.json') as direc:
    direc_dict = json.load(direc)
with open(direc_dict["custom"], 'r') as cus:
    custom_dict = json.load(cus)


class Events(commands.Cog):
    """Events that handle user errors and messages.
    No user commands added here... Yet.
    """
    def __init__(self, disclient):
        self.disclient = disclient

    @commands.Cog.listener()
    @commands.has_permissions(manage_messages=True)
    async def on_message(self, message):
        if message.author == self.disclient.user:
            return
        # user = message.author
        msg = message.content.split(" ")
        if msg[0].startswith("%"):
            with open(direc_dict["custom"], 'r') as cus:
                custom_dict = json.load(cus)
            command = msg[0].replace("%", "")
            print(command)
            if command in custom_dict["command_list"]:
                await message.channel.send(custom_dict["commands"][command])

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Permission denied!")
            raise error
        if isinstance(error, commands.CommandNotFound):
            async for message in ctx.history(limit=1):
                if message.author == self.disclient.user:
                    print("sent out a custom command")
                else:
                    print("Command not found!")
                    raise error

    # @commands.Cog.listener()
    # async def on_user_joins(self, ctx):


def setup(disclient):
    disclient.add_cog(Events(disclient))
