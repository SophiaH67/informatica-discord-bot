import discord
import os
from dotenv import load_dotenv
import glob
import importlib
from pathlib import Path
from urllib.parse import unquote
load_dotenv()

client = discord.Client()
cmds = {}
prefix = unquote(os.getenv("prefix"))
def load_commands():
    for commandFile in glob.glob("./cmds/*.py"):
        commandFilePath = Path(commandFile)
        command = __import__("cmds.{}".format(commandFilePath.stem), fromlist=["get_aliases", "run"])
        for alias in command.get_aliases():
            cmds[alias] = command.run

client.reload = load_commands

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))
    load_commands()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith(prefix):
        return
    args = message.content[len(prefix):].split(" ")
    command = args.pop(0)
    output = cmds[command](args, client)
    if type(output) is str:
        await message.channel.send(str(output))
    elif type(output) is discord.Embed:
        await message.channel.send(embed=output)

client.run(os.getenv("token"))