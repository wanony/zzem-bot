# import discord
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
        self.last_submissions = {}

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
                sub = reddit.subreddit(subreddit).new(limit=1)
                for subm in sub:
                    title = subm.title
                    if "/r/" in subm.url:
                        url = ""
                    else:
                        url = subm.url
                    auth = subm.author
                    perm = subm.permalink
                    if channel not in self.last_submissions:
                        updater = {channel: []}
                        self.last_submissions.update(updater)
                    if perm not in self.last_submissions[channel]:
                        self.last_submissions[channel].append(perm)
                        s = (f"`{auth}` posted `{title}` in **{subreddit}**!"
                             f" {url} \n"
                             f"<https://reddit.com{perm}>")
                        try:
                            await channel.send(s)
                        except AttributeError:
                            print("NoneType Error, check if channel deleted")

            for channel in reddit_dict:
                for subs in reddit_dict[channel]:
                    await post_to_server(channel, subs)
            await asyncio.sleep(180)

    @commands.command()
    async def unfollow_subreddit(self, ctx, subreddit):
        """Unfollow a previously followed subreddit"""
        channel = str(ctx.channel.id)
        subreddit = subreddit.lower()
        if str(channel) in reddit_dict:
            if subreddit in reddit_dict[channel]:
                reddit_dict[channel].remove(str(subreddit))
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
        channel = ctx.channel.id
        subreddit = subreddit.lower()
        if channel in reddit_dict:
            reddit_dict[channel].append(str(subreddit))
            await ctx.send(f"Added {subreddit} to this channel!")
        else:
            updater = {channel: [subreddit]}
            reddit_dict.update(updater)
            await ctx.send(f"Added {subreddit} to this channel!")


def setup(disclient):
    disclient.add_cog(Reddits(disclient))
