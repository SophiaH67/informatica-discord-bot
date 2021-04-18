def get_aliases():
    return ["reload","refresh","werk"]

def get_help():
    return "Reloads all commands"

def run(args, bot):
    bot.reload()
    return "Reloading all commands"