# import os
#
# # This is mandatory when executing the script in Spyder.
# if any('SPYDER' in name for name in os.environ):
#     import nest_asyncio
#     nest_asyncio.apply()
from sample.theBot import TheBot
from sample import poll
import constants as CST
# from bot_commands import load_commands, BotCommands
from discord.ext import commands

bot = TheBot()

wednesdayPollRoutine = \
    poll.TrainingPollRoutine("wednesday_training_poll",
                             "Wednesday training poll", bot,
                             poll.TrainingPollEmbedBuilder(2, 0x2A3AFF), "me")

saturdayPollRoutine = \
    poll.TrainingPollRoutine("saturday_training_poll",
                             "Saturday training poll", bot,
                             poll.TrainingPollEmbedBuilder(5, 0xFF5733), "sa")

bot.add_routine(wednesdayPollRoutine)
bot.add_routine(saturdayPollRoutine)
bot.run(CST.BOT_TOKEN)

# def main():
#     pass
#
#
# if __name__ == "__main__":
#     main()
