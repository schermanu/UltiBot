import babel.dates
import discord
import datetime
import constants as CST


def __init__():
    pass


# Builder of an embed that will serve as a poll for a given training.
class TrainingPollEmbedBuilder:

    def __init__(self, trainingDayNum, color):
        # Number of the week day on which the training occurs.
        self.trainingDayNum = trainingDayNum
        # Color to display with the message.
        self.color = color

    def build(self):
        # Calculate the date of the next training, for which to send the poll.
        trainingDate = get_date_from_weekday(self.trainingDayNum)
        trainingDateStr = \
            babel.dates.format_date(trainingDate, format='EEEE d MMMM', locale='fr_FR').capitalize()

        return \
            discord.Embed(
                title=f"! {trainingDateStr} !",
                description=
                "Préviens de ta présence à l'entraînement : \n"
                "✅ si tu viens\n"
                "☑️ seulement si on est assez pour des matchs\n"
                "❌ si tu viens pas\n"
                "❔ si tu sais pas encore",
                color=self.color)


# Routine that sends a poll for a training on a given channel, on a given day of the week.
class TrainingPollRoutine:

    def __init__(self, name, displayName, bot, embedBuilder):
        self.name = name
        self.displayName = displayName
        self.bot = bot
        self.embedBuilder = embedBuilder
        self.isEnabled = False
        self.executionDayNum = None
        self.channelId = None
        self.lastExecutionDate = None

    # Enable this routine and set the execution's day number.
    def enable(self, executionDayNum, channelId):
        self.executionDayNum = executionDayNum
        self.channelId = channelId
        self.lastExecutionDate = None
        self.isEnabled = True
        self.log("enabled")

    # Disable this routine.
    def disable(self):
        self.executionDayNum = None
        self.channelId = None
        self.isEnabled = False
        self.log("disabled")

    # If this routine is enabled, send a poll on the set channel,
    # if today is the set execution day.
    async def execute(self):

        channel = self.bot.get_channel(self.channelId)
        today = datetime.datetime.now(tz=CST.USER_TIMEZONE)
        alreadyExecutedToday = \
            False if self.lastExecutionDate is None \
            else (self.lastExecutionDate.date() == today.date())

        self.log(f"isEnabled = {self.isEnabled}")
        self.log(f"executionDayNum = {self.executionDayNum}")
        self.log(f"alreadyExecutedToday = {alreadyExecutedToday}")

        if self.isEnabled and today.weekday() == self.executionDayNum \
                and not alreadyExecutedToday:
            msg = await channel.send(embed=self.embedBuilder.build())
            await msg.add_reaction('✅')
            await msg.add_reaction('☑️')
            await msg.add_reaction('❌')
            await msg.add_reaction('❔')

            self.lastExecutionDate = datetime.datetime.now(tz=CST.USER_TIMEZONE)

    def log(self, msg):
        print(f"\t[routine \"{self.displayName}\"] {msg}")

    def save_state(self, state):

        state[self.name] = \
            {
                'isEnabled': "" if self.isEnabled is None else self.isEnabled,
                'execDayNum': "" if self.executionDayNum is None else self.executionDayNum,
                'channelId': "" if self.channelId is None else self.channelId,
                'lastExecDate': "" if self.lastExecutionDate is None else self.lastExecutionDate.isoformat(),
            }

    def load_state(self, state):

        if state.has_section(self.name):
            routineConfig = state[self.name]
            self.isEnabled = routineConfig.getboolean('isEnabled')
            self.executionDayNum = routineConfig.getint('execDayNum')
            self.channelId = routineConfig.getint('channelId')
            self.lastExecutionDate = routineConfig.getdatetime('lastExecDate')


# Get the date of the next day associated with the given week day number,
# from the given reference date. If none is provided, today is used.
def get_date_from_weekday(weekDayNum, refDate=None):
    if refDate is None:
        refDate = datetime.datetime.now(tz=CST.USER_TIMEZONE)
    daysBeforeTargetDay = (weekDayNum - refDate.weekday()) % 7
    return refDate + datetime.timedelta(days=daysBeforeTargetDay)


# Format the given time delta into a string.
def format_time_delta(delta: datetime.timedelta):
    res = ''
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds // 60) % 60
    seconds = delta.seconds % 60

    if days > 0: res += f'{days}j '
    if hours > 0: res += f'{hours}h '
    if minutes > 0: res += f'{minutes}m '
    if seconds > 0: res += f'{seconds}s '

    return res.strip()


# Get the name of the next day associated with the given week day number,
# from the given reference date. If none is provided, today is used.
def format_weekday_num(weekDayNum, format='EEEE', refDate=None):
    nextTargetDay = get_date_from_weekday(weekDayNum, refDate)
    return babel.dates.format_date(nextTargetDay, format=format)


def format_datetime(dateTime, placeholder='never', format='%d/%m/%Y, %H:%M:%S'):
    return placeholder if dateTime is None else dateTime.strftime(format)


