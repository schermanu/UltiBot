import asyncio
import datetime
from discord.ext import commands

from sample import poll
import constants as CST


def load_commands(bot, wednesdayPollRoutine, saturdayPollRoutine):

    # remplacer None par "0"
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
        channelId = CST.TEST_CHANNEL_ID if asTest else CST.TRAINING_POLLS_CHANNEL_ID
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
                isForTesting = 'yes' if routine.channelId == CST.TEST_CHANNEL_ID else 'no'
                msg += f'Routine "{routine.displayName}" enabled:\n' \
                       f'\t- execution day: {poll.format_weekday_num(routine.executionDayNum)}\n' \
                       f'\t- last execution: {poll.format_datetime(routine.lastExecutionDate)}\n' \
                       f'\t- for testing: {isForTesting}\n'
            else:
                msg += f'Routine "{routine.displayName}" disabled\n'

        await ctx.send(msg)


    @bot.command()
    async def react(ctx: commands.Context, msgId=1):
        await ctx.message.delete()
        if msgId == 1:
            msg_error = await ctx.send("need message id")
            await asyncio.sleep(2)
            await msg_error.delete()
        else:
            msg = await ctx.fetch_message(msgId)
            for reaction in msg.reactions:
                # await msg.clear_reaction(reaction.emoji)
                await msg.add_reaction(reaction.emoji)

    @bot.command(name="clear threads", description="supprimer les fils du channel")
    async def clearThreads(ctx: commands.Context):
        for thread in ctx.channel.threads:
            await thread.delete()

    @bot.command(name="test", descrtiption="commande de test")
    async def test(ctx: commands.Context):
        pass


