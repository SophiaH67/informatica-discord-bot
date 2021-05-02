from discord.ext import tasks, commands
from discord import Embed
import datetime
import arrow
from typing import List
from tzlocal import get_localzone
from hololive import hololive
import datetime
import time
from pygicord import Paginator

interested: List[str] = ["🎤","歌","sing","karaoke","asmr","ku100","archive","アーカイブなし","3d","3 d", "万"]
streams: List[hololive.Stream] = []
last_sync_unix: int = 0

async def sync() -> None:
  global last_sync_unix
  if int(time.time()) > (last_sync_unix + 30 * 60):
    global streams
    last_sync_unix = int(time.time())
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
  
  days = {}
  for stream in streams:
    if not any(term in stream.title_jp.lower() for term in interested):
      continue
    current_time = datetime.datetime.now()
    starttime = stream.starttime
    delta = round((starttime - current_time.replace(hour=starttime.hour, minute=starttime.minute, second=starttime.second)).days)
    try:
      days[delta]
    except:
      days[delta] = []
    days[delta].append(stream)

  pages = []
  offset_minutes = int(get_localzone().utcoffset(datetime.datetime.utcnow()).total_seconds() / 60) # offset from UTC in minutes
  for day, day_streams in days.items():
    e = Embed()
    e.color = 0x00FF00
    entries = []
    if day < -1:
      continue
    elif day == -1:
      e.title = "today"
    elif day == 0:
      e.title = "tomorrow"
    else:
      e.title = day
    for stream in day_streams:
      stream_starttime: arrow.Arrow = arrow.get(stream.starttime)
      entries.append("[{}]({})".format(stream.title_jp, stream.url))
      entries.append(stream.talent_jp)
      entries.append("{}({})".format(stream_starttime.humanize(), (stream.starttime + datetime.timedelta(minutes=offset_minutes)).strftime("%I:%M %p")))
      entries.append("")
    
    e.description = "\n".join(entries)    
    pages.append(e)
    
  paginator = Paginator(pages=pages, compact=True)
  await paginator.start(ctx)

def setup(bot: commands.bot.Bot):
  bot.add_command(run)

def teardown(bot: commands.bot.Bot):
  global last_sync_unix
  global hololive_schedule
  last_sync_unix = 0
  hololive_schedule = {}
