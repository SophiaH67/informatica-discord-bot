from discord.ext import commands
from discord import Embed
import TenGiphPy
import os

token = os.getenv("TENOR_TOKEN")
g = TenGiphPy.Tenor(token=token)

@commands.command(name="gif",aliases=["search"])
async def run(ctx, *query):
    try:
        url = g.random(tag=" ".join(query) )
    except KeyError:
        return await ctx.send("No tenor API token was provided. This functionality will not work")
    e = Embed(title=" ".join(query))
    e.set_image(url=url)

    return await ctx.send(embed=e)

def setup(bot):
    bot.add_command(run)