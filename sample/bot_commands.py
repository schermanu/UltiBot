import asyncio
import datetime

import discord
from discord.ext import commands

from sample import poll
import constants as CST
import io


# "name" parameter of a command is what need to be typed in discord to call it

def load_commands(bot: discord.Bot):
    # wednesdayPollRoutine, saturdayPollRoutine = None, None

    @bot.command(
        name='getlastmessage')
    async def client_getlastmessage(ctx, ID):
        """Get the last message of a text channel."""
        channel = bot.get_channel(int(ID))
        if channel is None:
            await ctx.send('Could not find that channel.')
            return
        # NOTE: get_channel can return a TextChannel, VoiceChannel,
        # or CategoryChannel. You may want to add a check to make sure
        # the ID is for text channels only

        message = await channel.fetch_message(
            channel.last_message_id)
        # NOTE: channel.last_message_id could return None; needs a check
        for i in range(20):
            await ctx.send(
                f'Last message in {channel.name} sent by {message.author.name}:\n'
                + message.content
            )
        await ctx.message.delete()

    @bot.command()
    async def set_poll_time(ctx: commands.Context, hoursStr, minutesStr=None, secondsStr=None):
        hours = int(hoursStr)
        minutes = 0 if minutesStr is None else int(minutesStr)
        seconds = 0 if secondsStr is None else int(secondsStr)
        triggerTime = datetime.time(hour=hours, minute=minutes, second=seconds)
        bot.set_routines_trigger_time(triggerTime)
        await bot.save_state()

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

        for routine in bot.routines:
            if routine.cmdKeyWord == trainingDayName:
                routine.enable(executionDayNum, channelId)
                continue

        await bot.save_state()

        await ctx.send(
            f'"{routine.displayName}" started{asTestMsg}. '
            f'Sending day is {poll.format_weekday_num(executionDayNum)}.')

    """Stop one message vote for mercredi or samedi. Enter the loop to stop : me or sa."""

    @bot.command()
    async def stop_poll(ctx: commands.Context, trainingDayName):

        dayNameNums = {'lu': 0, 'ma': 1, 'me': 2, 'je': 3, 've': 4, 'sa': 5, 'di': 6}

        if trainingDayName not in dayNameNums.keys():
            await ctx.send("The name provided for the training day is unknown.")
            return
        foundRoutine = False
        for routine in bot.routines:
            if routine.cmdKeyWord == trainingDayName:
                foundRoutine = True
                print(foundRoutine)
                routine.disable()
                await ctx.send(f'"{routine.displayName}" stopped.')
                await bot.save_state()
                continue
        if not foundRoutine:
            await ctx.send("No running routine for the training day provided.")


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

    @bot.command(name="clearThreads", description="supprimer les fils du channel")
    async def clearThreads(ctx: commands.Context):
        for thread in ctx.channel.threads:
            await thread.delete()
        await ctx.message.delete()

    @bot.command(name="test", descrtiption="commande de test")
    async def test(ctx: commands.Context):

        pass
        # async for message in ctx.channel.history(author=ctx.guild.get_member(913556318768463893)):
        #     print(message.created_at, message.author.name, message.content)
        # member = ctx.message.author
        # msg = discord.utils.get(await ctx.history(limit=100).flatten(), author=member)
        # await ctx.send(msg.author)
        # botMember = await ctx.channel.fetch_members(913556318768463893)

    @bot.command(name="copyMsg", descrtiption="copie le message ")
    async def copyMsg(ctx: commands.Context, msgId):
        msg = await ctx.fetch_message(msgId)
        await ctx.send(msg.content)

    # @bot.event
    # async def on_ready():
    #     print(f"nom utilisateur {bot.user.name}")

# class BotCommands(commands.Bot):
#     def __init__(self, bot: discord.Client):
#         super().__init__(command_prefix=commands.when_mentioned_or('?'))
#         load_commands(self, bot)
