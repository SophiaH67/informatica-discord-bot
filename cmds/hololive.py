import discord
import datetime

def get_aliases():
  return ["hololive","schedule","holoschedule"]

def get_help():
  return "Gets interesting streams from hololive"

def run(args, bot):
  e = discord.Embed(title="Hololive schedule")
  try:
    e.color = 0x00FF00
    for stream in bot.hololive_schedule:
      e.add_field(name=stream["title"], value="[{}]({})\n{}".format(stream["talent"], stream["url"],stream["datetime"].isoformat()))
  except AttributeError:
    e.add_field(name="Error", value="There was an error with the hololive API")
    e.color = 0xFF0000
  return e