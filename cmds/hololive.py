import discord
import datetime
import arrow
from typing import List
from tzlocal import get_localzone

def get_aliases():
  return ["hololive","schedule","holoschedule"]

def get_help():
  return "Gets interesting streams from hololive"

def run(args, bot):
  e = discord.Embed(title="Hololive schedule")
  try:
    for stream in bot.hololive_schedule:
      pass
  except AttributeError:
    e.add_field(name="Error", value="There was an error with the hololive API")
    e.color = 0xFF0000
    return e

  e.color = 0x00FF00
  entries = []
  current_day = -1
  current_time = datetime.datetime.now()
  
  for stream in bot.hololive_schedule:
    date: datetime.datetime = stream["datetime"]
    time = arrow.Arrow(date.year, date.month, date.day, date.hour, date.minute, date.second)
    
    if not current_day == date.day:
      current_day = date.day
      if not len(entries) == 0:
        entries.append("")
      diff = datetime.datetime(date.year, date.month, date.day, current_time.hour, current_time.minute, current_time.second) - current_time
      if diff.days < 0:
        entries.append("**today**")
      elif diff.days == 0:
        entries.append("**tomorrow**")
      else:
        entries.append("**in {} days".format(diff.days))
    offset_minutes = int(get_localzone().utcoffset(datetime.datetime.utcnow()).total_seconds() / 60)
    
    entries.append("**[{}]({})**".format(stream["title"], stream["url"]))
    entries.append(stream["talent"])
    entries.append("{}({})".format(time.humanize(), (stream["datetime"] + datetime.timedelta(minutes=offset_minutes)).strftime("%I:%M %p")))
      
  e.description = "\n".join(entries)
  return e
