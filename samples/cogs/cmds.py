import os

from disnake.ext import commands


def __init__(bot: commands.Bot):
    """
    This will automatically load slash commands and normal commands located in their respective folder.

    If you want to remove slash commands, which is not recommended due to the Message Intent being a privileged intent, you can remove the loading of slash commands below.
    """
    load_commands('normal', bot)
    load_commands('slash', bot)


def load_commands(command_type: str, bot: commands.Bot) -> None:
    for file in os.listdir(f"samples/cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"samples.cogs.{command_type}.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")
