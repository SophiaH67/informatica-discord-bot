from discord.ext import commands
from discord import Embed
import subprocess

@commands.command(name="version", help="Gets version number")
async def run(ctx: commands.context.Context):
  commit_hash = subprocess.check_output(["git", "describe", "--always"]).decode("utf-8")
  e = Embed(title="Current version")
  e.color = 0xFF00FF
  e.description = "I am currently running version [{0}](https://github.com/marnixah/informatica-discord-bot/commit/{0})".format(commit_hash)
  return await ctx.send(embed=e)

def setup(bot: commands.bot.Bot):
  bot.add_command(run)