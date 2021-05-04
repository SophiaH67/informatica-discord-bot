from pretty_help import PrettyHelp
from discord.ext import commands
import os
from dotenv import load_dotenv
import glob
import importlib
from pathlib import Path
from urllib.parse import unquote
import threading
load_dotenv()

prefix: str = unquote(os.getenv("PREFIX") or "?")
client: commands.bot.Bot = commands.Bot(command_prefix=prefix, help_command=PrettyHelp())


def load_commands():
  for commandFile in glob.glob("./cmds/*.py"):
    commandFilePath = Path(commandFile)
    command_path = "cmds.{}".format(commandFilePath.stem)
    client.load_extension(command_path)


def load_background_tasks():
  for commandFile in glob.glob("./bg/*.py"):
    commandFilePath = Path(commandFile)
    command_path = "bg.{}".format(commandFilePath.stem)
    client.load_extension(command_path)


@client.event
async def on_ready():
  print('Logged in as {}'.format(client.user))
  load_commands()
  load_background_tasks()
  if os.path.exists('/tmp/'):
    with open('/tmp/health', 'w') as file:
      file.write("ok")
try:
    client.run(os.getenv("TOKEN"))
except Exception as e:
  if os.path.exists('/tmp/health'):
    os.remove('/tmp/health')
  raise e