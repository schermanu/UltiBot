import discord
import datetime


def date_of_next_weekday(weekday):
    d = datetime.date.today()
    days_ahead = (weekday - d.weekday()) % 7
    next_training_day = d + datetime.timedelta(days_ahead)
    dic = {2: 'Mercredi', 5: 'Samedi'}
    training_day = dic[training_day_int]
    return training_day + ' ' + next_training_day.strftime('%d')
    # si on veut le mois, utiliser '%d.%m' le slash ne fonctionne pas


training_day_int = 5  # 0 = Monday, 1=Tuesday, 2=Wednesday...
thread_title = date_of_next_weekday(training_day_int)


Bot = discord.Client()


@Bot.event
async def on_message(ctx):
    if ctx.content == "!thread":
        channel = Bot.get_channel(913441193835257877)  # id de test2
        embed = discord.Embed(title=thread_title,
                              description="Préviens de ta présence à l'entraînement : \n"
                                          "✅ si tu viens\n"
                                          "☑️ seulement si on est assez pour des matchs\n"
                                          "❌ si tu viens pas\n"
                                          "❔ si tu sais pas encore",
                              color=0xFF5733)
        msg = await channel.send(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('☑️')
        await msg.add_reaction('❌')
        await msg.add_reaction('❔')

        f = await msg.create_thread(name=thread_title, auto_archive_duration=4320)
        await f.send("@licencié **Fil dédié à l'entraînement** (excuses bidons, covoit...)")


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
Bot.run(token)
