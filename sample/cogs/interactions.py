import asyncio

import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

import constants as CST


class Interactions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # --------------------- slash commands ---------------------
    # called using / in discord (they can take up to an hour to appear in discord)

    # @commands.slash_command(brief='This is the brief description',
    #                         description="Get the last message of a text channel")
    # async def get_last_message(self, ctx: discord.ApplicationContext,
    #                            identifiant: Option(str,
    #                                                description="id of the channel",
    #                                                required=True,
    #                                                default=None)):
    #     """Get the last message of a text channel."""
    #     channel = ctx.bot.get_channel(int(identifiant))
    #     if channel is None:
    #         await ctx.respond('Could not find that channel.')
    #         return
    #
    #     message = await channel.fetch_message(
    #         channel.last_message_id)
    #     # NOTE: channel.last_message_id could return None; needs a check
    #
    #     await ctx.respond(
    #         f'Last message in {channel.name} sent by {message.author.name}:\n'
    #         + message.content)
    #
    #     # await ctx.message.delete()

    @commands.slash_command(
        description="Copy the reactions of a given message.")
    async def react(self, ctx: discord.ApplicationContext,
                    message_id: Option(str,
                                       description="Id of the message (need to activate dev option,"
                                                   "then copy id on the message options)",
                                       required=True,
                                       default=1)):
        await ctx.message.delete()
        if message_id == 1:
            msg_error = await ctx.respond("need message id")
            await asyncio.sleep(2)
            await msg_error.delete()
        else:
            msg = await ctx.fetch_message(message_id)

            for reaction in msg.reactions:
                await msg.add_reaction(reaction.emoji)
                # remove the reactions made by the author of the message
                async for user in reaction.users():
                    if user == ctx.message.author:
                        await msg.remove_reaction(reaction.emoji, user)

    @commands.slash_command(description="Clear everything in the test channel")
    async def clean_test_channel(self, ctx: discord.ApplicationContext):
        respond = await ctx.respond("working...")
        for thread in ctx.bot.get_channel(CST.TEST_CHANNEL_ID).threads:
            await thread.delete()
        for msg in await ctx.bot.get_channel(CST.TEST_CHANNEL_ID).history().flatten():
            await msg.delete()

    @commands.slash_command(description="hello test")
    async def tes(self, ctx: discord.ApplicationContext):
        await ctx.respond("coucou tes")

    @commands.slash_command(description="stop l'archivage du fil")
    async def stop_archiving(self, ctx: discord.ApplicationContext,
                  given_name: Option(str,
                                       description="Id of the message (need to activate dev option,"
                                                   "then copy id on the message options)",
                                       required=False,
                                       default=None)):
        # await ctx.respond("coucou tes")
        threadId = None
        if given_name is None:
            if ctx.channel.type.value == 11:  # type 11 corresponds to thread channels
                threadId = ctx.channel.id
            else:
                respond = await ctx.send("This channel is not a thread. "
                                         "Consider writing this command into a thread, or give the thread"
                                         " name as argument.")
        else:
            try:
                if not given_name.isdigit():
                    given_name = given_name.replace('<', '').replace('>', '').replace('#', '')
                threadId = int(given_name)
                thread = ctx.bot.get_channel(threadId)
                if thread.type.value == 11:
                    threadId = thread.id
                else:
                    respond = await ctx.send("Given channel is not a thread. "
                                             "Consider writing this command into a thread, "
                                             "or give the thread name as argument.")
            except:
                respond = await ctx.respond("couldn't find the channel")

        if threadId is not None:
            if ctx.bot.protectedThreads.count(threadId) == 0:
                ctx.bot.protectedThreads.append(threadId)
                await ctx.bot.reset_archiving_timer()
                respond = await ctx.send("Thread added !")
            else:
                respond = await ctx.send("Thread already registered")

        await asyncio.sleep(5)
        await ctx.message.delete()
        await respond.delete()


    # --------------------- normal commands ---------------------
    # called using ? in discord

    # @commands.command(name="copy_msg", descrtiption="copie le message ")
    # async def copy_msg(self, ctx: commands.Context, msgId):
    #     msg = await ctx.fetch_message(msgId)
    #     await ctx.send(msg.content)

    @commands.command(descrtiption="Copy the reactions of a given message.")  # for polls
    async def react(self, ctx: commands.Context):
        if ctx.message.reference is None:
            warning = await ctx.reply("❌ The command message needs to be a response of the message to react to.")
            await asyncio.sleep(5)
            await warning.delete()
        else:
            msg = await ctx.fetch_message(ctx.message.reference.resolved.id)
            for reaction in msg.reactions:
                await msg.add_reaction(reaction.emoji)
                # remove the reactions made by the author of the message
                async for user in reaction.users():
                    if user == ctx.message.author:
                        await msg.remove_reaction(reaction.emoji, user)

        await ctx.message.delete()
        # async for message in ctx.channel.history(author=ctx.guild.get_member(913556318768463893)):
        #     print(message.created_at, message.author.name, message.content)
        # member = ctx.message.author
        # msg = discord.utils.get(await ctx.history(limit=100).flatten(), author=member)
        # await ctx.send(msg.author)
        # botMember = await ctx.channel.fetch_members(913556318768463893)

    @commands.command(descrtiption="Allow threads to avoid being archived")
    async def stop_archiving(self, ctx: commands.Context, threadIdStr=None):
        threadId = None
        if threadIdStr is None:
            if ctx.channel.type.value == 11:  # type 11 corresponds to thread channels
                threadId = ctx.channel.id
        else:
            try:
                if not threadIdStr.isdigit():
                    threadIdStr = threadIdStr.replace('<', '').replace('>', '').replace('#', '')
                threadId = int(threadIdStr)
                thread = ctx.bot.get_channel(threadId)
                if not thread.type.value == 11:
                    threadId = None
            except:
                threadId = None

        if threadId is not None:
            if ctx.bot.protectedThreads.count(threadId) == 0:
                ctx.bot.protectedThreads.append(threadId)
                await ctx.bot.reset_archiving_timer()
                respond = await ctx.send("Thread added !")
            else:
                respond = await ctx.send("Thread already registered")
        else:
            respond = await ctx.send("This channel is not a thread. "
                                     "Consider writing this command into a thread, or give the thread id as argument.")
        await asyncio.sleep(5)
        await ctx.message.delete()
        await respond.delete()


def setup(bot):
    bot.add_cog(Interactions(bot))
