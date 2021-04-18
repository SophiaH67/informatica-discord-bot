import discord
import TenGiphPy
import os

token = os.getenv("TENOR_TOKEN")
g = TenGiphPy.Tenor(token=token)

def get_aliases():
    return ["gif"]

def get_help():
    return "Searches and sends a GIF with query"

def run(args, bot):
    try:
        url = g.random(tag=" ".join(args) )
    except KeyError:
        return "No tenor API token was provided. This functionality will not work"
    e = discord.Embed(title=" ".join(args))
    e.set_image(url=url)

    return e