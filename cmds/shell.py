from discord.ext import commands
from discord import Embed

bot:commands.bot.Bot = None

@commands.command(name="shell", help="Opens a python interactive shell")
@commands.has_permissions(administrator=True)
async def run(ctx: commands.context.Context):
  await ctx.send(">>>")
  def check(message):
    return message.author.id == ctx.author.id
  while True:
    try:
      msg = await bot.wait_for('message', check=check, timeout=30)
    except TimeoutError:
      return await ctx.send("Exited shell(timeout)")
    output = await exec_code(msg.content)
    if not output:
      await ctx.send("Exited shell succesfully")
      break
    messages = []
    current_message = ""
    words = output.split()
    for i in range(len(words)):
      word = words[i]
      if len(current_message + word) >= 2000:
        messages.append(current_message)
        current_message = ""
      current_message += "" if len(current_message) == 0 else " "
      current_message += word
      if i == (len(words)-1):
        messages.append(current_message)
    for message in messages:
      await ctx.send(message)

async def exec_code(code) -> str:
  try:
    exec("global tmp; tmp = " + code)
    global tmp
    output = tmp.decode("utf-8")
  except Exception as e:
    output = str(e)
  if output == "None" or output == "":
    output = ":white_check_mark:"
  if output == ".exit":
    output == ""
  return output
@run.error
async def run_error(error, ctx):
  if isinstance(error, commands.CheckFailure):
    e = Embed(title="Permission denied!")
    e.color = 0xFF0000
    e.description = "You need to be an administrator to use this command"
    await ctx.send(embed=e)

def setup(client: commands.bot.Bot):
  global bot
  bot = client
  client.add_command(run)