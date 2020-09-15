import discord
import json
import praw
from discord.ext import commands
import asyncio

with open('directories.json') as direc:
    direc_dict = json.load(direc)
with open(direc_dict["apis"], 'r') as apis:
    apis_dict = json.load(apis)
with open(direc_dict["reddit"], 'r') as redd:
    reddit_dict = json.load(redd)

reddit = praw.Reddit(client_id=apis_dict["reddit_id"],
                     client_secret=apis_dict["reddit_secret"],
                     user_agent="idk what this is")


class Reddits(commands.Cog):
    """Get new posts from your favourite Subreddits
    """
    def __init__(self, disclient):
        self.disclient = disclient
        self.disclient.loop.create_task(self.post_new())
        self.disclient.loop.create_task(self.write_reddit())

    @commands.Cog.listener()
    async def write_reddit(self):
        await self.disclient.wait_until_ready()
        while not self.disclient.is_closed():
            with open(direc_dict["reddit"], 'w') as red:
                json.dump(reddit_dict, red, indent=4)
            await asyncio.sleep(5)

    @commands.Cog.listener()
    async def post_new(self):
        await self.disclient.wait_until_ready()
        while not self.disclient.is_closed():

            async def post_to_server(channel, subreddit):
                channel = self.disclient.get_channel(int(channel))
                chanid = str(channel.id)
                sub = reddit.subreddit(subreddit).new(limit=1)
                for subm in sub:
                    titl = subm.title
                    if "/r/" in subm.url:
                        url = ""
                    else:
                        url = subm.url
                    auth = subm.author
                    perm = subm.permalink
                    fts = (".JPG", ".jpg", ".JPEG", ".jpeg", ".PNG", ".png")
                    gifs = (
                        "https://gfycat.com/",
                        "https://www.redgifs.com/",
                        "https://www.gifdeliverynetwork.com/"
                    )
                    if reddit_dict[chanid][subreddit]["last_post"] == perm:
                        pass
                    else:
                        soy = "https://reddit.com"
                        reddit_dict[chanid][subreddit]["last_post"] = perm
                        desc = f"Posted by {auth} in **/r/{subreddit}**"
                        embed = discord.Embed(title=titl,
                                              description=desc,
                                              color=discord.Color.blurple())
                        if url:
                            val = f"{soy}{perm} \n**{url}**"
                            if url.endswith(fts):
                                embed.set_image(url=url)
                                # val = f"{soy}{perm} \n**{url}**"
                                embed.add_field(name="Post Permalink",
                                                value=val)
                                try:
                                    await channel.send(embed=embed)
                                except AttributeError:
                                    print("Channel deleted")
                            elif url.startswith(gifs):
                                # val = f"{soy}{perm} \n**{url}**"
                                embed.add_field(name="Post Permalink",
                                                value=val)
                                try:
                                    await channel.send(embed=embed)
                                    await channel.send(url)
                                except AttributeError:
                                    print("Channel deleted")
                            else:
                                val = f"{soy}{perm}"
                                embed.add_field(name="Post Permalink",
                                                value=val)
                                try:
                                    await channel.send(embed=embed)
                                    await channel.send(url)
                                except AttributeError:
                                    print("Channel deleted")
                        else:
                            val = f"{soy}{perm}"
                            embed.add_field(name="Post Permalink",
                                            value=val)
                            try:
                                await channel.send(embed=embed)
                            except AttributeError:
                                print("Channel deleted")

            for channel in reddit_dict:
                for subs in reddit_dict[channel]:
                    await post_to_server(channel, subs)
            await asyncio.sleep(180)

    @commands.command()
    async def unfollow_subreddit(self, ctx, subreddit):
        """Unfollow a previously followed subreddit"""
        channel = str(ctx.channel.id)
        subreddit = subreddit.lower()
        if channel in reddit_dict:
            print("channel in dict")
            if subreddit in reddit_dict[channel]:
                print("sub in channel")
                del reddit_dict[channel][subreddit]
                if not reddit_dict[channel]:
                    del reddit_dict[channel]
                await ctx.send(f"Unfollowed {subreddit} in this channel!")
            else:
                await ctx.send(f"{subreddit} is not followed in this channel")
        else:
            await ctx.send("No subreddits are followed in this channel")

    @commands.command()
    async def follow_subreddit(self, ctx, subreddit):
        """Add a subreddit to follow in this server!
        The channel this command is invoked in will be used
        to post the new submission to the sub"""
        channel = str(ctx.channel.id)
        subreddit = subreddit.lower()
        if channel in reddit_dict:
            updater = {subreddit: {"last_post": ""}}
            reddit_dict[channel].update(updater)
            await ctx.send(f"Added {subreddit} to this channel!")
        else:
            updater = {channel: {subreddit: {"last_post": ""}}}
            reddit_dict.update(updater)
            await ctx.send(f"Added {subreddit} to this channel!")


def setup(disclient):
    disclient.add_cog(Reddits(disclient))
