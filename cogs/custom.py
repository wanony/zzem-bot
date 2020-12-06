from discord.ext import commands
from data import GetCommands
from data import AddCommand
from data import RemoveCommand


class Custom(commands.Cog):
    """This category contains commands that can be made
    by users that are for fun, such a their own memes or
    reaction gfys or youtube links.
    """

    def __init__(self, disclient):
        self.disclient = disclient

    @commands.command(aliases=['delcommand', 'dc'])
    @commands.has_any_role('Moderator', 'Admin')
    async def delete_command(self, ctx, command):
        """MOD: Removes a custom command created previously"""
        command = command.lower()
        removed = RemoveCommand(command)
        if removed:
            await ctx.send(f"Custom command: `{command}` removed.")
        else:
            await ctx.send(f"Custom command: `{command}` could not be found.")

    @commands.command(aliases=['commands'])
    async def command_list(self, ctx):
        """Sends a list of all the custom commands"""
        command_list = GetCommands().keys()
        if len(command_list) == 0:
            await ctx.send(f"No commands have been added.")
        else:
            await ctx.send(f"`{'`, `'.join(command_list)}`")

    @commands.command(aliases=['ac', 'addcommand'])
    async def add_command(self, ctx, name, gfy):
        """
        Adds a custom command with a valid gfy/red/gif link!
        Example: .addcommand fun <link>
        You can now call this command with .fun
        """
        name = name.lower()
        valid = (
            "https://gfycat.com/",
            "https://www.youtube.com/",
            "https://redgifs.com/",
            "https://www.gifdeliverynetwork.com/"
        )
        # We call get_commands here for now, should likely have single
        # entry fetch.
        command_list = GetCommands()
        if name in command_list:
            await ctx.send(
                "Command name already exists! Try a different name.")
        elif "." in name:
            await ctx.send("Illegal character `.` in command name!")
        elif gfy.startswith(valid):
            AddCommand(name, gfy, ctx.author.id)
            await ctx.send(f"Command: `.{name}` added!")
        else:
            await ctx.send(
                "Link invalid, use gfycat, redgifs, gifdeliverynet or youtube")


def setup(disclient):
    disclient.add_cog(Custom(disclient))
