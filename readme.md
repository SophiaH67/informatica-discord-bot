# informatica-discord-bot

## Running

In order to run this bot, you first need [a working docker install](https://docs.docker.com/get-started/). And at the very least [a discord bot token](https://discordpy.readthedocs.io/en/latest/discord.html)

```bash
docker run -it -d \
  --name "informatica-discord-bot" `#Name of the container`\
  -e TOKEN="Your token here" `#Your 59 character discord token` \
  -e PREFIX="!" \
  -e TENOR_TOKEN="" `#OPTIONAL if you want to use the gif functionality` \
  marnixah/informatica-discord-bot:latest
```

Your discord bot should then come online and you should be able to use it with the prefix you defined in the variable.
