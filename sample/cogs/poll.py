import datetime
import asyncio
import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

from sample import poll
import constants as CST


class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="set the poll committing time")
    async def set_poll_time(self, ctx: commands.Context, hoursStr, minutesStr=None, secondsStr=None):
        hours = int(hoursStr)
        minutes = 0 if minutesStr is None else int(minutesStr)
        seconds = 0 if secondsStr is None else int(secondsStr)
        triggerTime = datetime.time(hour=hours, minute=minutes, second=seconds)
        await ctx.bot.set_routines_trigger_time(triggerTime)
        await ctx.bot.save_state()
        # await ctx.respond(f"Polls sending time set to {triggerTime}.")
        await ctx.send(f"Polls sending time set to {triggerTime}.")

    """Starts one message vote for lundi, mercredi or samedi.
    Enter the loop to start: lu, me or sa, and the day to send the vote """

    @commands.command(brief="start a poll")
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

    @commands.command(brief="stop the given poll")
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

    @commands.command(brief="return some info about the polls")
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

    @commands.command(brief="add a training to cancel")
    async def canceled_training(self, ctx: commands.Context, date, reason):

        if date.replace('/', '').isdigit():
            ctx.bot.canceledTrainings[date] = reason
            response = await ctx.send(f"l'entraitnement du {date} est enregistré comme annulé car {reason}")
        else:
            response = await ctx.send("le format de date entré est incorrect (dd/mm)")
        await ctx.bot.save_state()
        await asyncio.sleep(5)
        await ctx.message.delete()
        await response.delete()

    @commands.command(brief="Remove training date from canceled list")
    async def remove_canceled_training(self, ctx: commands.Context, date):

        if date.replace('/', '').isdigit():
            del ctx.bot.canceledTrainings[date]
            response = await ctx.send(f"l'entraitnement du {date} a été retiré")
        else:
            response = await ctx.send("le format de date entré est incorrect (dd/mm)")
        await ctx.bot.save_state()
        await asyncio.sleep(5)
        await ctx.message.delete()
        await response.delete()


training_commands_group = SlashCommandGroup(name="trainings", description="Commands related to training poll")


@training_commands_group.command(name="add_canceled_date", brief="add a training to cancel",
                                 description="add a training date to save as canceled")
async def _add_canceled_date(ctx: discord.ApplicationContext,
                             date: Option(str,
                                          description="date (format dd/mm)",
                                          required=True),
                             reason: Option(str,
                                            description="entraînement annulé car:",
                                            required=True)):
    if date.replace('/', '').isdigit() and len(date) == 5:
        ctx.bot.canceledTrainings[date] = reason
        response = await ctx.respond(f"l'entrainement du {date} est enregistré comme annulé car {reason}")
    else:
        response = await ctx.respond("le format de date entré est incorrect (dd/mm)")
    await ctx.bot.save_state()


@training_commands_group.command(name="remove_canceled_date", brief="Remove training date from canceled list",
                                 description="Remove date from canceled trainings list")
async def _remove_canceled_date(ctx: discord.ApplicationContext,
                                    date: Option(str,
                                                 description="date (format dd/mm)",
                                                 required=True)):
    if date.replace('/', '').isdigit() and len(date) == 5:
        if ctx.bot.canceledTrainings.get(date) is not None:
            del ctx.bot.canceledTrainings[date]
            response = await ctx.respond(f"l'entrainement du {date} a été retiré")
        else:
            response = await ctx.respond(f"l'entrainement du {date} n'est pas dans la liste")
    else:
        response = await ctx.respond("le format de date entré est incorrect (dd/mm)")
    await ctx.bot.save_state()


def setup(bot):
    bot.add_cog(Poll(bot))
    bot.add_application_command(training_commands_group)
    pass
