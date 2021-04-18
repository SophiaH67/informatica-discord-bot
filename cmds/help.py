import discord
def get_aliases():
    return ["help"]

def get_help():
    return "Shows this message"

def run(args, bot):
    e = discord.Embed(title="Help")
    e.color = 0x0000FF
    for command, help_message in bot.help:
        e.add_field(name=command, value=help_message)
    return e
    