import discord
import datetime
import asyncio


def date_of_next_weekday(weekday):
    d = datetime.date.today()
    days_ahead = (weekday - d.weekday()) % 7
    next_training_day = d + datetime.timedelta(days_ahead)
    dic = {2: 'Mercredi', 5: 'Samedi'}
    training_day = dic[training_day_int]
    return training_day + ' ' + next_training_day.strftime('%d')
    # si on veut le mois, utiliser '%d.%m' le slash ne fonctionne pas


training_day_int = 5  # 0 = Monday, 1=Tuesday, 2=Wednesday...
embed_title = date_of_next_weekday(training_day_int)


Bot = discord.Client()


@Bot.event
async def on_message(ctx):
    if ctx.content == "!test":
        channel = Bot.get_channel(913433889345769572)  # id de test1
        counter = 0
        counter_archived = 0
        for thread in channel.threads:
            if not thread.archived:
                await thread.edit(auto_archive_duration=60)
                await thread.edit(auto_archive_duration=4320)
                counter += 1
            else:
                counter_archived += 1
        await channel.send(f"{counter} fils ont étés prolongés et {counter_archived} fils sont archivés")# msg1 = await channel.send('hey1')
        # duration = 60
        # # f = await msg1.create_thread(name=embed_title, auto_archive_duration=duration)
        # # await f.send("bla")
        # msg2 = await channel.send('hey2')
        # g = await msg2.create_thread(name=embed_title, auto_archive_duration=duration)
        # await g.send("bla")
        # print(g.archive_timestamp)
        # h = await g.edit(name="bla", archived=True)
        # # await asyncio.sleep(1)
        # i = await h.edit(name="bla", archived=False, auto_archive_duration=60)
        # j = await g.edit(name="bla", auto_archive_duration=60)
        # print(g.archive_timestamp)
        # await Bot.wait_until_ready()
        # await asyncio.sleep(1)
        # # g.thread_update(auto_archive_duration=60)
        # h = Bot.get_channel(g.id)
        #
        # print(h.archive_timestamp)

    if ctx.content == "!clearThread":
        for thread in ctx.channel.threads:
            await thread.delete()

    if ctx.content == "!t":
        pass




def read_token():
    with open("unusedFiles/token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
Bot.run(token)
