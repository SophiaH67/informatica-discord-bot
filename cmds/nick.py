from discord.ext import commands
from discord import Embed
import subprocess

@commands.command(name="nick", help="Changes bot nickname")
async def run(ctx: commands.context.Context, nickname: str):
  await ctx.guild.me.edit(nick=nickname)
  e = Embed(title="Success!")
  e.color = 0x00FF00
  e.description = f"Succesfully set nickname to {nickname}"
  return await ctx.send(embed=e)

def setup(bot: commands.bot.Bot):
  bot.add_command(run)