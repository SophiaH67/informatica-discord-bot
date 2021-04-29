from discord.ext import commands
import os
from dotenv import load_dotenv
import glob
import importlib
from pathlib import Path
from urllib.parse import unquote
import threading
load_dotenv()
from pretty_help import PrettyHelp

prefix = unquote(os.getenv("prefix"))
client = commands.Bot(command_prefix=prefix, help_command=PrettyHelp())
def load_commands():
    for commandFile in glob.glob("./cmds/*.py"):
        commandFilePath = Path(commandFile)
        command_path = "cmds.{}".format(commandFilePath.stem)
        client.load_extension(command_path)

def load_background_tasks():
    for backgroundTask in glob.glob("./bg/*.py"):
        backgroundTaskPath = Path(backgroundTask)
        background = __import__("bg.{}".format(backgroundTaskPath.stem), fromlist=["run"])
        thread = threading.Thread(target=background.start, args=(client,))
        thread.daemon = True
        thread.start()

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))
    load_commands()
    load_background_tasks()

client.run(os.getenv("token"))