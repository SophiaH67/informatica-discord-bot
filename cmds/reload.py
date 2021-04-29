from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotLoaded
client = None

@commands.command(name="reload", aliases=["refresh","werk"])
async def run(ctx, command=""):
    try:
        client.reload_extension(f"cmds.{command}")
    except ExtensionNotLoaded:
        return await ctx.send(f"Unable to reload{command}")
    return await ctx.send(f"Reloading {command} command!")

def setup(bot):
    global client
    client = bot
    bot.add_command(run)