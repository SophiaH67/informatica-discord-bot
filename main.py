import discord
import os
from dotenv import load_dotenv
import glob
import importlib
from pathlib import Path
from urllib.parse import unquote
import threading
load_dotenv()

client = discord.Client()
cmds = {}
client.help = {}
prefix = unquote(os.getenv("prefix"))
def load_commands():
    for commandFile in glob.glob("./cmds/*.py"):
        commandFilePath = Path(commandFile)
        command_path = "cmds.{}".format(commandFilePath.stem)
        command = __import__(command_path, fromlist=["get_aliases", "run"])
        aliases = command.get_aliases()
        client.help[aliases[0]] = command.get_help()
        for alias in aliases:
            cmds[alias] = command.run

def load_background_tasks():
    for backgroundTask in glob.glob("./bg/*.py"):
        backgroundTaskPath = Path(backgroundTask)
        background = __import__("bg.{}".format(backgroundTaskPath.stem), fromlist=["run"])
        thread = threading.Thread(target=background.start, args=(client,))
        thread.daemon = True
        thread.start()

client.reload = load_commands

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))
    load_commands()
    load_background_tasks()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith(prefix):
        return
    args = message.content[len(prefix):].split(" ")
    command = args.pop(0)
    if not command in cmds:
        return
    output = cmds[command](args, client)
    if type(output) is str:
        await message.channel.send(str(output))
    elif type(output) is discord.Embed:
        await message.channel.send(embed=output)

client.run(os.getenv("token"))