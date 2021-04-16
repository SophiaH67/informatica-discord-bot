import discord
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

client.run(os.getenv("token"))