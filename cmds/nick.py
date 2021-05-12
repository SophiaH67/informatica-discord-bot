from discord.ext import commands
from discord import Embed
from typing import Tuple

@commands.command(name="nick", help="Changes bot nickname")
async def run(ctx: commands.context.Context, *nickname: Tuple[str, ...]):
  nick = " ".join(nickname)
  await ctx.guild.me.edit(nick=nick)
  e = Embed(title="Success!")
  e.color = 0x00FF00
  e.description = f"Succesfully set nickname to {nick}"
  return await ctx.send(embed=e)

def setup(bot: commands.bot.Bot):
  bot.add_command(run)