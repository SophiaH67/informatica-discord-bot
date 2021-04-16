def get_aliases():
    return ["reload","refresh","werk"]

def run(args, bot):
    bot.reload()
    return "Reloading all commands"