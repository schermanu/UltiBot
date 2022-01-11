import datetime

import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

from sample import poll
import constants as CST


class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_poll_time(self, ctx: commands.Context, hoursStr, minutesStr=None, secondsStr=None):
        hours = int(hoursStr)
        minutes = 0 if minutesStr is None else int(minutesStr)
        seconds = 0 if secondsStr is None else int(secondsStr)
        triggerTime = datetime.time(hour=hours, minute=minutes, second=seconds)
        ctx.bot.set_routines_trigger_time(triggerTime)
        await ctx.bot.save_state()
        # await ctx.respond(f"Polls sending time set to {triggerTime}.")
        await ctx.send(f"Polls sending time set to {triggerTime}.")

    """Starts one message vote for lundi, mercredi or samedi.
    Enter the loop to start: lu, me or sa, and the day to send the vote """

    @commands.command()
    async def start_poll(self, ctx: commands.Context, trainingDayName, executionDayName, asTestStr=None):

        dayNameNums = {'lu': 0, 'ma': 1, 'me': 2, 'je': 3, 've': 4, 'sa': 5, 'di': 6}

        if trainingDayName not in dayNameNums.keys():
            await ctx.send("The name provided for the training day is unknown.")
            return

        if executionDayName not in dayNameNums.keys():
            await ctx.send("The name provided for the routine's execution day is unknown.")
            return

        executionDayNum = dayNameNums[executionDayName]
        asTest = False if asTestStr is None else (asTestStr.lower() == "test")
        channelId = CST.TEST_CHANNEL_ID if asTest else CST.TRAINING_POLLS_CHANNEL_ID
        asTestMsg = " for testing" if asTest else ""

        for routine in ctx.bot.routines:
            if routine.cmdKeyWord == trainingDayName:
                routine.enable(executionDayNum, channelId)
                await ctx.send(
                    f'"{routine.displayName}" started{asTestMsg}. '
                    f'Sending day is {poll.format_weekday_num(executionDayNum)}.')

        await ctx.bot.save_state()

    """Stop one message vote for lundi, mercredi or samedi. Enter the loop to stop : lu, me or sa."""

    @commands.command()
    async def stop_poll(self, ctx: commands.Context, trainingDayName):

        dayNameNums = {'lu': 0, 'ma': 1, 'me': 2, 'je': 3, 've': 4, 'sa': 5, 'di': 6}

        if trainingDayName not in dayNameNums.keys():
            await ctx.send("The name provided for the training day is unknown.")
            return

        for routine in ctx.bot.routines:
            if routine.cmdKeyWord == trainingDayName:
                foundRoutine = True
                print(foundRoutine)
                routine.disable()
                await ctx.send(f'"{routine.displayName}" stopped.')
                await ctx.bot.save_state()
                break

    @commands.command()
    async def status(self, ctx: commands.Context):
        triggerTimeStr = ctx.bot.routinesTriggerTime.strftime("%H:%M:%S")
        timeUntilTriggerStr = poll.format_time_delta(ctx.bot.get_time_until_routines_trigger())
        lastRoutinesTriggerDateStr = poll.format_datetime(ctx.bot.lastRoutinesTriggerDate)

        msg = f'Start time: {poll.format_datetime(ctx.bot.routinesTaskStartTime)}\n' \
              f'Poll time: {triggerTimeStr} ({timeUntilTriggerStr} before next trigger)\n' \
              f'Last routines trigger: {lastRoutinesTriggerDateStr}\n'

        for routine in ctx.bot.routines:
            if routine.isEnabled:
                isForTesting = 'yes' if routine.channelId == CST.TEST_CHANNEL_ID else 'no'
                msg += f'Routine "{routine.displayName}" enabled:\n' \
                       f'\t- execution day: {poll.format_weekday_num(routine.executionDayNum)}\n' \
                       f'\t- last execution: {poll.format_datetime(routine.lastExecutionDate)}\n' \
                       f'\t- for testing: {isForTesting}\n'
            else:
                msg += f'Routine "{routine.displayName}" disabled\n'

        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Poll(bot))
