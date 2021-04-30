from discord.ext import commands
from discord import Embed
from discord.ext.commands.context import Context
import TenGiphPy
import os

token = os.getenv("TENOR_TOKEN")
g = TenGiphPy.Tenor(token=token)

@commands.command(name="gif",aliases=["search"], help="Searches and sends a GIF with query")
async def run(ctx: Context, *query: tuple[str, ...]):
    print(type(query))
    full_query = " ".join(''.join(word) for word in query)
    try:
        url = g.random(tag=full_query)
    except KeyError:
        return await ctx.send("No tenor API token was provided. This functionality will not work")
    except IndexError:
        return await ctx.send("Couldn't find any gifs with the query \"{}\"".format(full_query))
    e = Embed(title=full_query)
    e.set_image(url=url)

    return await ctx.send(embed=e)

def setup(bot):
    bot.add_command(run)