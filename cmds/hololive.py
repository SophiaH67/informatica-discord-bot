from discord.ext import tasks, commands
from discord import Embed
import datetime
import arrow
from typing import List
from tzlocal import get_localzone
import requests
import datetime
import time
import urllib
import json
import cutlet
katsu = cutlet.Cutlet()
katsu.use_foreign_spelling = False
interested = ["🎤","歌","sing","karaoke","asmr","ku100","archive","アーカイブなし","3d","3 d", "万"]
hololive_schedule = {}
last_sync_unix = 0

def sync():
  global last_sync_unix
  if (last_sync_unix + 30 * 60) > int(time.time()):
    return
  last_sync_unix = int(time.time())
  global hololive_schedule
  raw_schedule = requests.get("https://hololive-api.marnixah.com/").json()
  streams = []
  for day in raw_schedule["schedule"]:
    date_month = day["date"].split("/")[0]
    date_day = day["date"].split("/")[1]
    for stream in day["schedules"]:
      stream_dict = {}
      stream["youtube_url"]
      
      if not any(term in stream["title"].lower() for term in interested):
        continue
      
      stream_dict["title"] = katsu.romaji(stream["title"])
      stream_dict["url"] = stream["youtube_url"]
      stream_dict["talent"] = katsu.romaji(stream["member"])

      time_arr = stream["time"].split(":")
      hour = int(time_arr[0])
      minute = int(time_arr[1])

      current_time = datetime.datetime.utcnow()
      year = current_time.year

      stream_dict["datetime"] = datetime.datetime(
        year, int(date_month), int(date_day), hour, minute
      ) - datetime.timedelta(hours=9)  # JST is 9 hours ahead of UTC
      
      streams.append(stream_dict)
  hololive_schedule = streams

@commands.command(name="hololive", aliases=["schedule","holoschedule"], help="Gets interesting streams from hololive")
async def run(ctx):
  global hololive_schedule
  try:
    sync()
  except:
    e = Embed(title="Hololive schedule")
    e.add_field(name="Error", value="There was an error with the hololive API")
    e.color = 0xFF0000
    return await ctx.send(embed=e)

  entries = []
  current_day = -1
  current_time = datetime.datetime.now()
  
  for stream in hololive_schedule:
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

  e = Embed(title="hololive schedule")
  for entry in entries:
    e.color = 0x00FF00
    if len(str(e.description) + entry) > 2000:
      await ctx.send(embed=e)
      e = Embed()
    e.description = str(e.description) + "\n" + entry

def setup(bot):
  bot.add_command(run)

def teardown(bot):
  global last_sync_unix
  global hololive_schedule
  last_sync_unix = 0
  hololive_schedule = {}