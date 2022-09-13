
import disnake
from disnake.ext import commands

from samples.helpers import DatabaseManager

class TheBot(commands.Bot):
    def __init__(self, config):
        self.config = config["discord"]
        self.db = DatabaseManager(config["mySQL"])

        """	
        Setup bot intents (events restrictions)
        For more information about intents, please go to the following websites:
        https://docs.disnake.dev/en/latest/intents.html
        https://docs.disnake.dev/en/latest/intents.html#privileged-intents


        Default Intents:
        intents.bans = True
        intents.dm_messages = True
        intents.dm_reactions = True
        intents.dm_typing = True
        intents.emojis = True
        intents.emojis_and_stickers = True
        intents.guild_messages = True
        intents.guild_reactions = True
        intents.guild_scheduled_events = True
        intents.guild_typing = True
        intents.guilds = True
        intents.integrations = True
        intents.invites = True
        intents.messages = True # `message_content` is required to get the content of the messages
        intents.reactions = True
        intents.typing = True
        intents.voice_states = True
        intents.webhooks = True

        Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
        intents.members = True
        intents.message_content = True
        intents.presences = True
        """

        intents = disnake.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned_or(self.config["prefix"]), case_insensitive=False,
                         intents=intents, help_command=None)
