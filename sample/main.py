#
# # This is mandatory when executing the script in Spyder.
# if any('SPYDER' in name for name in os.environ):
#     import nest_asyncio
#     nest_asyncio.apply()
import theBot
import poll
import constants as CST


bot = theBot.TheBot()

embedDescription = "Préviens de ta présence à l'entraînement : \n" \
                   "✅ si tu viens\n" \
                   "☑️que si on est assez pour des matchs\n" \
                   "❌ si tu viens pas\n" \
                   "❔ si tu sais pas encore"
reactions = ["✅", "☑", "❌", "❔"]
threadMsgStr = "**Fil de discussion dédié à cet entraînement**"
# threadMsgStr = f"<@&{CST.LICENCIE_ROLE_ID}>\n**Fil de discussion dédié à cet entraînement**"

wednesdayPollRoutine = \
    poll.TrainingPollRoutine("wednesday_training_poll",
                             "Wednesday training poll", bot,
                             poll.TrainingPollMsgBuilder(2, embedDescription, reactions, 0x2A3AFF, threadMsgStr), "me")

saturdayPollRoutine = \
    poll.TrainingPollRoutine("saturday_training_poll",
                             "Saturday training poll", bot,
                             poll.TrainingPollMsgBuilder(5, embedDescription, reactions, 0xFF5733, threadMsgStr), "sa")

bot.add_routine(wednesdayPollRoutine)
bot.add_routine(saturdayPollRoutine)

bot.param.stateHeader = "#state#\n#sauvegarde de l'état du bot\n"  # will be written by the bot
bot.param.configHeader = "#config#"  # will not be written by the bot

bot.run(CST.BOT_TOKEN)

# def main():
#     pass
#
#
# if __name__ == "__main__":
#     main()
