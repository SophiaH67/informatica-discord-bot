import discord
import datetime

def get_aliases():
  return ["hololive","schedule","holoschedule"]

def run(args, bot):
  e = discord.Embed(title="Hololive schedule")
  for stream in bot.hololive_schedule:
    e.add_field(name=stream["title"], value="[{}]({})\n{}".format(stream["talent"], stream["url"],stream["datetime"].isoformat()))
  return e