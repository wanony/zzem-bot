import discord
import json
import datetime
import shutil
import threading
import os
from discord.ext import commands
with open('directories.json') as direc:
    direc_dict = json.load(direc)
with open(direc_dict["apis"], 'r') as apis:
    json_dict = json.load(apis)
with open(direc_dict["gfys"], 'r') as gfys:
    gfys_dict = json.load(gfys)
with open(direc_dict["levels"], 'r') as usrs:
    users = json.load(usrs)
path_to_images = direc_dict["images"]
cog_path = direc_dict["cogs"]

# intents = discord.Intents()
# intents.members = True

disclient = commands.Bot(command_prefix='.')  # , intents=intents)
# for when it comes for a custom help command
disclient.remove_command('help')
# commands.DefaultHelpCommand(width=100, dm_help=True, dm_help_threshold=100)


@disclient.event
async def on_ready():
    await disclient.change_presence(status=discord.Status.online)
    print(f"bot is online as {disclient.user.name}!")


def backup_gfy_file():
    shutil.copyfile(direc_dict["gfys"], './backupgfys/backupgfys.json')
    print("gfys backed up at " + str(datetime.datetime.now()))
    threading.Timer(3600.0, backup_gfy_file).start()


def backup_users_file():
    shutil.copyfile(direc_dict["levels"], './backupgfys/backuplvls.json')
    print("users backed up at " + str(datetime.datetime.now()))
    threading.Timer(3600.0, backup_users_file).start()


try:
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                disclient.load_extension(cog)
                print(cog)
            except Exception:
                print(f"Failed to load {cog}")
except OSError:
    print("No cogs to load!")


backup_gfy_file()
backup_users_file()
disclient.run(json_dict["discord_token"])
