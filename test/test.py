import asyncio
import datetime

from discord.commands import Option, SlashCommandGroup
import discord
from discord.ext import commands
from discord import guild
# from discord_slash import SlashCommand, SlashContext
# from discord_slash.utils.manage_commands import create_choice, create_option
import constants as CST



bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'),intents=discord.Intents.all())



# @bot.event
# async def on_ready():
#     pass
#     # msg = await bot.get_channel(CST.TEST_CHANNEL_ID).send("heu")
#     # f = await msg.create_thread(name="prpu", auto_archive_duration=CST.MAX_THREAD_ARCHIVING_DURATION)
#     # role = discord.utils.get(msg.guild.roles, name="licencié")
#     # # # user = bot.get_user()
#     # msg = await f.send(role.mention)
#
#     # await msg.delete()
#     # await f.join()
#     # for member in msg.channel.members:
#     #     if member.id == 853998598617432064:
#     #         print("found manu")
#     #     await f.add_user(member)
#     #     notif = f.last_message
#     #     await notif.delete()
#     # rolesearch = discord.utils.get(msg.guild.roles,
#     #                                name="licencié")
#
#
#
#
#
#
# #
# #
# # # slash = SlashCommand(bot, sync_commands=True)
# #
# # # name = 'getlastmessage',
# # # description = "Get the last message of a text channel.",
# # # guild_ids = 884913501968158720
# # @bot.slash_command(description="Stuck? Use ME!")
# # async def lol(ctx: discord.ApplicationContext):
# #     """Get help about the most feature packed bot!!"""
# #
# #     await ctx.respond("embed=Help_Embed(), view=HelpOptions()")
# #     message = await ctx.interaction.original_message()
# #     await asyncio.sleep(5)
# #     try:
# #         await message.edit("This help session expired", embed=None, view=None)
# #     except:
# #         pass
# #
# # @bot.slash_command(description="prout Prout")
# # async def prout(ctx: discord.ApplicationContext):
# #     """Get help about the most feature packed bot!!"""
# #
# #     await ctx.respond("caca")
# #
#
#
#
#
#
# #working slashfunctions
# groupe = SlashCommandGroup(name="cat", description="Commands related to your ass")
#
# @groupe.command(name="blab", description="bouh!")
# async def tesin(ctx: discord.ApplicationContext):
#     await ctx.respond("blabla")
#
#
# @groupe.command(name="blabreponse", description="bouh 2!")
# async def rep(ctx: discord.ApplicationContext, txt: Option(str, description="superu")):
#     await ctx.respond(f"blabla : {txt}")
#
#
# @bot.slash_command()
# async def test(ctx):
#     await ctx.send("hello")
#
#
# @bot.slash_command(description="hello test")
# async def tes(ctx: discord.ApplicationContext):
#     await ctx.respond("coucou tes")
#
#
# @bot.slash_command(name="clean_test_channel", description="supprime le contenu du salon de test")
# async def clean_test_channel(ctx: commands.Context):
#     respond = await ctx.respond("working...")
#     for thread in bot.get_channel(CST.TEST_CHANNEL_ID).threads:
#         await thread.delete()
#     for msg in await bot.get_channel(CST.TEST_CHANNEL_ID).history().flatten():
#         await msg.delete()
#     # respond.delete()
#     # await ctx.message.delete()
#
# # @bot.event
# # async def on_ready():
# #     print("ready")
#
#
# bot.add_application_command(groupe)
#


bot.run(CST.BOT_TOKEN)
