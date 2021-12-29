
import datetime
# import os
#
# # This is mandatory when executing the script in Spyder.
# if any('SPYDER' in name for name in os.environ):
#     import nest_asyncio
#     nest_asyncio.apply()

from discord.ext import commands
import asyncio
import configparser
from backports import zoneinfo

from sample import poll

# Path to the file describing the state in which to start the bot.
STATE_FILE_PATH = "../state.ini"
# Identifier of the Discord channel dedicated to training polls.
TRAINING_POLLS_CHANNEL_ID = 913522652239519775
# Identifier of the Discord channel dedicated to tests.
TEST2_CHANNEL_ID = 913441193835257877
# Maximum duration of any sleep (in seconds).
# IMPORTANT: there seems to be a bug with asyncio, making that any wait longer
# than 24 hours (ie. 86400 seconds) never actually ends. That's why this setting
# exists and should always be less than 86400.
MAX_SLEEP_DURATION = 3600
# Time zone to use when receiving dates from the user, or displaying them to him.
USER_TIMEZONE = zoneinfo.ZoneInfo("Europe/Paris")


# Parser of the bot's state. Allows to save and restore its state after a reboot.
class BotState(configparser.ConfigParser):

    def __init__(self):
        super().__init__(
            converters=
            {
                'int': self.parse_int,
                'datetime': self.parse_iso_datetime,
                'time': self.parse_time,
            })

    def parse_int(self, s):
        try:
            return int(s)
        except (ValueError, TypeError):
            return None

    def parse_iso_datetime(self, s):
        try:
            return datetime.datetime.fromisoformat(s)
        except (ValueError, TypeError):
            return None

    def parse_time(self, s):
        try:
            return datetime.time.fromisoformat(s)
        except (ValueError, TypeError):
            return None


# The bot that receives all commands.
class TheBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('?'))
        self.state = BotState()
        self.routines = []
        self.routinesTask = None
        self.routinesTaskStartTime = None
        # By giving no argument, this will be midnight by default.
        self.routinesTriggerTime = datetime.time()
        self.lastRoutinesTriggerDate = None

    def add_routine(self, routine):
        self.routines.append(routine)
        return self

    def set_routines_trigger_time(self, triggerTime):
        self.routinesTriggerTime = triggerTime
        self.restart_routines_task()
        return self

    def get_next_trigger_date(self):
        now = datetime.datetime.now(tz=USER_TIMEZONE)
        triggerDate = datetime.datetime.combine(now, self.routinesTriggerTime, tzinfo=USER_TIMEZONE)
        # If the trigger time has passed for today, consider tomorrow's trigger time.
        if triggerDate < now:
            triggerDate += datetime.timedelta(days=1)
        return triggerDate

    def get_time_until_routines_trigger(self):
        return self.get_next_trigger_date() - datetime.datetime.now(tz=USER_TIMEZONE)

    def restart_routines_task(self):

        if self.routinesTask is not None:
            self.routinesTask.cancel()

        self.log("restarting routines task")
        self.routinesTask = self.loop.create_task(self.run_routines())

    async def on_ready(self):

        self.log(f'Logged in as {self.user} (ID: {self.user.id})')
        self.load_state()

        # If a routines trigger time is set.
        # DISABLED: since the script is currently hosted on Heroku, and Heroku
        # restarts its virtual hosts every day (resetting the state file),
        # we don't want the bot to think it missed the last trigger on every reboot.
        if False and self.routinesTriggerTime is not None:

            # Calculate the date of the previous trigger,
            # which is the date of the next trigger minus one day,
            # since the routines are triggered once a day.
            previousTriggerDate = self.get_next_trigger_date() - datetime.timedelta(days=1)

            # If the last routines trigger happened before the supposed previous trigger date,
            # that means the bot missed a trigger, so try to make up for it
            # by running the routines now.
            if (self.lastRoutinesTriggerDate is None
                    or self.lastRoutinesTriggerDate < previousTriggerDate):
                await self.run_routines_once()

        self.restart_routines_task()

    async def run_routines(self):

        await self.wait_until_ready()

        self.routinesTaskStartTime = datetime.datetime.now(tz=USER_TIMEZONE)

        while not self.is_closed():

            waitDuration = self.get_time_until_routines_trigger().seconds

            self.log(f"waiting until {self.routinesTriggerTime}")

            # Wait until the next trigger time, while checking in regularly
            # to avoid a bug with asyncio, that makes a wait never end, when
            # it's longer than 24 hours.
            while waitDuration > 0:
                timeUntilNextCheckin = min(waitDuration, MAX_SLEEP_DURATION)
                await asyncio.sleep(timeUntilNextCheckin)
                waitDuration -= timeUntilNextCheckin

            await self.run_routines_once()

            # This is to ensure not to spam routines during the second
            # that is just right on the trigger time.
            await asyncio.sleep(1)

    async def run_routines_once(self):

        self.log("executing routines")
        self.lastRoutinesTriggerDate = datetime.datetime.now(tz=USER_TIMEZONE)

        for routine in self.routines:
            await routine.execute()

        self.save_state()

    def log(self, msg):
        print(f"[bot] {msg}")

    def save_state(self):

        self.state['bot'] = \
            {
                'routinesTriggerTime':
                    "" if self.routinesTriggerTime is None
                    else self.routinesTriggerTime.isoformat(),
                'lastRoutinesTriggerDate':
                    "" if self.lastRoutinesTriggerDate is None
                    else self.lastRoutinesTriggerDate.isoformat(),
            }

        for routine in self.routines:
            routine.save_state(self.state)

        with open(STATE_FILE_PATH, "w+") as stateFile:
            self.state.write(stateFile)

    def load_state(self):

        self.state.read(STATE_FILE_PATH)

        if self.state.has_section('bot'):

            botConfig = self.state['bot']
            self.routinesTriggerTime = botConfig.gettime('routinesTriggerTime')
            self.lastRoutinesTriggerDate = botConfig.getdatetime('lastRoutinesTriggerDate')

            for routine in self.routines:
                routine.load_state(self.state)


# Read the bot token contained in the file located at the given path.
def read_bot_token(filePath):
    with open(filePath, "r") as f:
        lines = f.readlines()
        f.close()
        return lines[0].strip()


bot = TheBot()

wednesdayPollRoutine = \
    poll.TrainingPollRoutine("wednesday_training_poll",
                             "Wednesday training poll", bot,
                             poll.TrainingPollEmbedBuilder(2, 0x2A3AFF))

saturdayPollRoutine = \
    poll.TrainingPollRoutine("saturday_training_poll",
                             "Saturday training poll", bot,
                             poll.TrainingPollEmbedBuilder(5, 0xFF5733))


@bot.command()
async def set_poll_time(ctx: commands.Context, hoursStr, minutesStr=None, secondsStr=None):
    hours = int(hoursStr)
    minutes = 0 if minutesStr is None else int(minutesStr)
    seconds = 0 if secondsStr is None else int(secondsStr)
    triggerTime = datetime.time(hour=hours, minute=minutes, second=seconds)

    bot.set_routines_trigger_time(triggerTime)
    bot.save_state()

    await ctx.send(f"Polls sending time set to {triggerTime}.")


"""Starts one message vote for mercredi or samedi.
Enter the loop to start: me or sa, and the day to send the vote """


@bot.command()
async def start_poll(ctx: commands.Context, trainingDayName, executionDayName, asTestStr=None):
    dayNameNums = {'lu': 0, 'ma': 1, 'me': 2, 'je': 3, 've': 4, 'sa': 5, 'di': 6}

    if trainingDayName not in dayNameNums.keys():
        await ctx.send("The name provided for the training day is unknown.")
        return

    if executionDayName not in dayNameNums.keys():
        await ctx.send("The name provided for the routine's execution day is unknown.")
        return

    executionDayNum = dayNameNums[executionDayName]
    asTest = False if asTestStr is None else (asTestStr.lower() == "test")
    channelId = TEST2_CHANNEL_ID if asTest else TRAINING_POLLS_CHANNEL_ID
    asTestMsg = " for testing" if asTest else ""
    routine = None

    if trainingDayName == 'me':
        routine = wednesdayPollRoutine
    elif trainingDayName == 'sa':
        routine = saturdayPollRoutine

    routine.enable(executionDayNum, channelId)
    bot.save_state()

    await ctx.send(
        f'"{routine.displayName}" started{asTestMsg}. '
        f'Sending day is {poll.format_weekday_num(executionDayNum)}.')


"""Stop one message vote for mercredi or samedi. Enter the loop to stop : me or sa."""


@bot.command()
async def stop_poll(ctx: commands.Context, trainingDayName):
    if trainingDayName == 'me':
        routine = wednesdayPollRoutine
    elif trainingDayName == 'sa':
        routine = saturdayPollRoutine
    else:
        await ctx.send("The name provided for the training day is unknown.")
        return

    routine.disable()
    bot.save_state()

    await ctx.send(f'"{routine.displayName}" stopped.')


@bot.command()
async def status(ctx: commands.Context):
    triggerTimeStr = bot.routinesTriggerTime.strftime("%H:%M:%S")
    timeUntilTriggerStr = poll.format_time_delta(bot.get_time_until_routines_trigger())
    lastRoutinesTriggerDateStr = poll.format_datetime(bot.lastRoutinesTriggerDate)

    msg = f'Start time: {poll.format_datetime(bot.routinesTaskStartTime)}\n' \
          f'Poll time: {triggerTimeStr} ({timeUntilTriggerStr} before next trigger)\n' \
          f'Last routines trigger: {lastRoutinesTriggerDateStr}\n'

    for routine in bot.routines:
        if routine.isEnabled:
            isForTesting = 'yes' if routine.channelId == TEST2_CHANNEL_ID else 'no'
            msg += f'Routine "{routine.displayName}" enabled:\n' \
                   f'\t- execution day: {poll.format_weekday_num(routine.executionDayNum)}\n' \
                   f'\t- last execution: {poll.format_datetime(routine.lastExecutionDate)}\n' \
                   f'\t- for testing: {isForTesting}\n'
        else:
            msg += f'Routine "{routine.displayName}" disabled\n'

    await ctx.send(msg)


@bot.command()
async def react(ctx: commands.Context, msgId=None):
    if msgId == 1:
        msg = await ctx.channel.history(limit=2).flatten()[1]
    else:
        msg = await ctx.fetch_message(msgId)

    for reaction in msg.reactions:
        # await msg.clear_reaction(reaction.emoji)
        await msg.add_reaction(reaction.emoji)

    await ctx.message.delete()


def main():
    bot.add_routine(wednesdayPollRoutine)
    bot.add_routine(saturdayPollRoutine)

    bot.run(read_bot_token("../unusedFiles/token.txt"))


if __name__ == "__main__":
    main()
