# from backports import zoneinfo
import datetime

import arrow
# Constantes utilisées par le bot, pour éviter de les écrire dans le code
# une variable par ligne, sans commentaires sur la ligne

# le token est le mode d'authentification du client Python au serveur Discord
BOT_TOKEN = "OTEzNTU2MzE4NzY4NDYzODkz.YaANnw.XaW1ixXbQx5fZt2FYoXVgjM7kPI"

# id du salon discord dédié au paramétrage du bot #paramètres-du-bot
CONFIG_CHANNEL_ID = 925507525992931378

# Identifier of the Discord channel dedicated to training polls.
TRAINING_POLLS_CHANNEL_ID = 913522652239519775

# Identifier of the Discord channel dedicated to tests.
TEST_CHANNEL_ID = 925875143895547964

# Path to the file describing the state in which to start the bot.
STATE_FILE_PATH = "../state.ini"

# Maximum duration of any sleep (in seconds).
# IMPORTANT: there seems to be a bug with asyncio, making that any wait longer
# than 24 hours (ie. 86400 seconds) never actually ends. That's why this setting
# exists and should always be less than 86400.
MAX_SLEEP_DURATION = 3600
# Time zone to use when receiving dates from the user, or displaying them to him.

from dateutil import tz
USER_TIMEZONE = tz.gettz('Europe/Paris')
# zoneinfo.ZoneInfo("Europe/Paris")


