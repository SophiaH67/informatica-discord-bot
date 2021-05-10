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

### Tenor token

In order to obtain a tenor api token. Go to [the tenor developer dashboard](https://tenor.com/developer/dashboard), make an account, then create an app with any title and description. You will get a key which you can put in the TENOR_TOKEN environment variable
