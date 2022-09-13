""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json
import os
import platform
import random
import sys

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context

import samples
from samples import TheBot
print(os.path)
# os.path.join(path, *paths)

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


bot = TheBot(config)


@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    # samples.cogs.cmds.__init__(bot)
    samples.events.__init__(bot)
    samples.loops.__init__(bot)
    print(f"Logged in as {bot.user.name}")
    print(f"disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()
    # find_new_poll_routines_task.start()



@tasks.loop(minutes=1.0)
async def status_task() -> None:
    bot.db.log_db(bot)




if __name__ == "__main__":
    pass


# Run the bot with the token
bot.run(config["discord"]["token"])
