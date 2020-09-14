import discord
import json
from discord.ext import commands
with open('directories.json') as direc:
    direc_dict = json.load(direc)
with open(direc_dict["levels"], 'r') as usrs:
    users = json.load(usrs)
path_to_images = direc_dict["images"]
cog_path = direc_dict["cogs"]


class General(commands.Cog):
    """General commands that are useful to get
    information about users or help!
    """
    def __init__(self, disclient):
        self.disclient = disclient

    # Shamelessly stolen from Jared Newsom (AKA Jared M.F.)
    # https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b
    # Refactored into flake8 linting
    @commands.command(pass_context=True)
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self, ctx, *cog):
        """Gets all cogs and commands of mine."""
        if not cog:
            titl = 'Category List'
            desc = ('Use `.help <Category>` to find out more about them! \n'
                    '(BTW, the Category Name Must Be in Title Case, Just '
                    'Like this Sentence.')
            halp = discord.Embed(title=titl,
                                 description=desc,
                                 color=discord.Color.blurple())
            cogs_desc = ''
            for x in self.disclient.cogs:
                docu = self.disclient.cogs[x].__doc__
                x = f"`{x}`"
                cogs_desc += ('{} - {}'.format(x, docu)+'\n')
            halp.add_field(name='Categories',
                           value=cogs_desc[0:len(cogs_desc)-1],
                           inline=False)
            cmds_desc = ''
            for y in self.disclient.walk_commands():
                if not y.cog_name and not y.hidden:
                    cmds_desc += ('{} - {}'.format(y.name, y.help) + '\n')
            # removed as no commands are uncategorised
            # halp.add_field(name='Uncatergorized Commands',
            #                value=cmds_desc[0:len(cmds_desc)-1],
            #                inline=False)
            await ctx.message.add_reaction(emoji='✉')
            await ctx.message.author.send(embed=halp)
        else:
            if len(cog) > 1:
                halp = discord.Embed(title='Error!',
                                     description='Too many cogs!',
                                     color=discord.Color.red())
                await ctx.message.author.send(embed=halp)
            else:
                found = False
                for x in self.disclient.cogs:
                    for y in cog:
                        if x == y:
                            titl = f"{cog[0]} Command List"
                            desc = self.disclient.cogs[cog[0]].__doc__
                            halp = discord.Embed(title=titl,
                                                 description=desc,
                                                 color=discord.Color.blurple())
                            cmnd = self.disclient.get_cog(y).get_commands()
                            for c in cmnd:
                                if not c.hidden:
                                    halp.add_field(name=c.name,
                                                   value=c.help,
                                                   inline=False)
                            found = True
                if not found:
                    errr = f'Cog {cog[0]} not found!'
                    halp = discord.Embed(title='Error!',
                                         description=errr,
                                         color=discord.Color.red())
                else:
                    await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send(embed=halp)

    @commands.command(aliases=['avatar'])
    async def get_avatar(self, ctx, member: discord.Member = None):
        """returns the users avatar"""
        if member:
            member = member
        else:
            member = ctx.author
        embed = discord.Embed(colour=member.colour)
        embed.set_author(name=f"{member}")
        # embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"requested by {ctx.author}",
                         icon_url=ctx.author.avatar_url)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['profile'])
    async def user_profile(self, ctx, member: discord.Member = None):
        """returns some user information"""
        if member:
            member = member
        else:
            member = ctx.author
        print(member)
        cr_at = member.created_at.strftime("%a, %#d %B %Y, %I:%M%p UTC")
        jo_at = member.joined_at.strftime("%a, %#d %B %Y, %I:%M%p UTC")
        embed = discord.Embed(colour=member.colour)
        embed.set_author(name=member)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}",
                         icon_url=ctx.author.avatar_url)
        embed.add_field(name="Level:",
                        value=users[str(member.id)]['level'])
        embed.add_field(name="XP:", value=users[str(member.id)]['xp'])
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Account Created:", value=cr_at)
        embed.add_field(name="Joined Server:", value=jo_at)
        await ctx.send(embed=embed)


def setup(disclient):
    disclient.add_cog(General(disclient))
