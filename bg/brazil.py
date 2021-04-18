import discord
import time
import random

def start(bot: discord.Client):
  @bot.event
  async def on_message(message):
    if random.randrange(0,10) > 8:
      await message.channel.send("Go to brazil {} you stinky monkey".format(message.author.mention))