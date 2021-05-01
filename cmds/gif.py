from discord.ext import commands
from discord import Embed
from discord.ext.commands.context import Context
from typing import Tuple
import TenGiphPy
import os

token: str = os.getenv("TENOR_TOKEN") or ""
g: TenGiphPy.Tenor = TenGiphPy.Tenor(token=token)

@commands.command(name="gif",aliases=["search"], help="Searches and sends a GIF with query")
async def run(ctx: commands.context.Context, *query: Tuple[str, ...]):
    full_query = " ".join(''.join(word) for word in query)
    try:
        url: str = g.random(tag=full_query)
    except KeyError:
        return await ctx.send("No tenor API token was provided. This functionality will not work")
    except IndexError:
        return await ctx.send("Couldn't find any gifs with the query \"{}\"".format(full_query))
    e: Embed = Embed(title=full_query)
    e.set_image(url=url)
    return await ctx.send(embed=e)

def setup(bot: commands.bot.Bot):
    bot.add_command(run)