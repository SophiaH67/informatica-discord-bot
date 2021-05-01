from discord.ext import tasks, commands
from discord import Embed
import datetime
import arrow
from typing import List
from tzlocal import get_localzone
from hololive import hololive
import datetime
import time
interested: List[str] = ["🎤","歌","sing","karaoke","asmr","ku100","archive","アーカイブなし","3d","3 d", "万"]
streams: List[hololive.Stream] = []
last_sync_unix = 0

async def sync() -> None:
  if int(time.time()) > (last_sync_unix + 30 * 60):
    global streams
    streams = await hololive.get_streams()

@commands.command(name="hololive", aliases=["schedule","holoschedule"], help="Gets interesting streams from hololive")
async def run(ctx: commands.context.Context):
  global streams
  try:
      await sync()
  except:
    e = Embed(title="Hololive schedule")
    e.add_field(name="Error", value="There was an error with the hololive API")
    e.color = 0xFF0000
    return await ctx.send(embed=e)

  entries = []
  current_day = -1
  current_time = datetime.datetime.now()
  
  for stream in streams:
    if not any(term in stream.title_jp.lower() for term in interested):
        continue
    date: datetime.datetime = stream.starttime
    time: arrow.Arrow = arrow.Arrow(date.year, date.month, date.day, date.hour, date.minute, date.second)
    
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
    
    entries.append("**[{}]({})**".format(stream.title_jp, stream.url))
    entries.append(stream.talent_jp)
    entries.append("{}({})".format(time.humanize(), (stream.starttime + datetime.timedelta(minutes=offset_minutes)).strftime("%I:%M %p")))

  embeds: List[Embed] = []
  e = Embed(title="hololive schedule")
  e.description = ""
  
  for i in range(len(entries)):
    entry: str = entries[i]
    e.color = 0x00FF00
    if len(str(e.description) + entry) > 2000:
      embeds.append(e)
      e = Embed()
      e.description = ""
    e.description += "\n" + entry
    if i+1 == len(entries):
      embeds.append(e)
  for embed in embeds:
    await ctx.send(embed=embed)
  

def setup(bot: commands.bot.Bot):
  bot.add_command(run)

def teardown(bot: commands.bot.Bot):
  global last_sync_unix
  global hololive_schedule
  last_sync_unix = 0
  hololive_schedule = {}