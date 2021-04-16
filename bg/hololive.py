import requests
import datetime
import time
import urllib
import json
import cutlet
katsu = cutlet.Cutlet()
katsu.use_foreign_spelling = False


interested = ["🎤","歌","sing","karaoke","asmr","ku100","archive","アーカイブなし","3d","3 d"]

def start(bot):
  sync(bot)
  print("Synced hololive schedule!")
  while True:
    time.sleep(30 * 60)
    sync(bot)


def sync(bot):
  raw_schedule = requests.get("https://hololive-api.marnixah.com/").json()
  streams = []
  for day in raw_schedule["schedule"]:
    date_month = day["date"].split("/")[0]
    date_day = day["date"].split("/")[1]
    for stream in day["schedules"]:
      stream_dict = {}
      title =  get_youtube_title(stream["youtube_url"])
      
      if not any(term in title.lower() for term in interested):
        continue
      
      stream_dict["title"] = katsu.romaji(title)
      
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
  bot.hololive_schedule = streams

def get_youtube_title(youtube_url):
    params = {"format": "json", "url": youtube_url}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    with urllib.request.urlopen(req) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return data['title']