import discord
from discord.ext import commands
import json
import asyncio
with open('directories.json') as direc:
    direc_dict = json.load(direc)
with open(direc_dict["apis"], 'r') as apis:
    json_dict = json.load(apis)
with open(direc_dict["custom"], 'r') as cus:
    custom_dict = json.load(cus)
with open(direc_dict["gfys"], 'r') as gfys:
    gfys_dict = json.load(gfys)
with open(direc_dict["levels"], 'r') as usrs:
    users = json.load(usrs)
path_to_images = direc_dict["images"]


class Levels(commands.Cog):
    """Levels, XP, and contribution handling commands found here
    will let users get information about levels and leaderboards
    of the top contributors!
    """
    def __init__(self, disclient):
        self.disclient = disclient
        self.disclient.loop.create_task(self.write_people())

    @commands.Cog.listener()
    async def write_people(self):
        await self.disclient.wait_until_ready()
        while not self.disclient.is_closed():
            with open(direc_dict["levels"], 'w') as lev:
                json.dump(users, lev, indent=4)
            await asyncio.sleep(5)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.disclient.user:
            return
        if message.author.bot:
            return
        author = str(message.author.id)
        if author not in users:
            users[author] = {}
            users[author]['level'] = 1
            users[author]['xp'] = 0
        users[author]['xp'] += 1
        if self.level_up(author):
            embed = discord.Embed(colour=message.author.colour,
                                  title="Level Up!!")
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name="Level:", value=users[author]['level'])
            embed.add_field(name="XP:", value=users[author]['xp'])
            await message.channel.send(embed=embed)

    def level_up(self, author):
        current_xp = users[author]['xp']
        current_lvl = users[author]['level']
        if current_xp >= current_lvl * 100:
            users[author]['level'] += 1

    @commands.command(aliases=['xp'])
    async def level(self, ctx, member: discord.Member = None):
        """Returns information of the users level"""
        print("called level command")
        if member:
            member = member
        else:
            member = ctx.author
        if str(member.id) in users:
            embed = discord.Embed(colour=member.colour, title="Level & XP")
            embed.set_author(name=member)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"Requested by {ctx.author}",
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Level:",
                            value=users[str(member.id)]['level'])
            embed.add_field(name="XP:", value=users[str(member.id)]['xp'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Member has no XP!")

    @commands.command()
    async def leaderboard(self, ctx):
        """
        Returns a leaderboard of the top 10 contributers!
        This leaderboard is made from all contributers across
        every server the bot is connected to.
        """
        with open(direc_dict["contri"]) as cont:
            uz = json.load(cont)
        listo = {}
        for member in uz:
            memberid = await self.disclient.fetch_user(member)
            cont = uz[member]["cont"]
            thing = {str(memberid): cont}
            listo.update(thing)
        p = {k: v for k, v in sorted(listo.items(),
                                     key=lambda item: item[1],
                                     reverse=True)}
        embed = discord.Embed(title="Contribution Leaderboard",
                              description="",
                              color=discord.Color.blurple())
        e = 1
        spacing = " "
        for elem in p:
            elem = f"{elem} {p[elem]}"
            elem = elem.split(" ")
            nam = ' '.join(elem[:-1])
            elem = f"{nam}{spacing*(29 - len(nam))}{elem[-1]}"
            embed.add_field(name="-", value=f"`{e}. {elem}`", inline=False)
            e += 1
        await ctx.send(embed=embed)


def format_list(array):
    formatted = ''.join(array)
    return formatted


def setup(disclient):
    disclient.add_cog(Levels(disclient))
