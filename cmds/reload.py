from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotLoaded
client: commands.bot.Bot = None

@commands.command(name="reload", aliases=["refresh","werk"], help="Reloads a specified command")
async def run(ctx: commands.context.Context, command:str=""):
    try:
        client.reload_extension(f"cmds.{command}")
    except ExtensionNotLoaded:
        return await ctx.send(f"Unable to reload {command}")
    return await ctx.send(f"Reloading {command} command!")

def setup(bot: commands.bot.Bot):
    global client
    client = bot
    bot.add_command(run)