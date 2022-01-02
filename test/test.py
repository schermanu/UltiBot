import asyncio
import datetime

from discord.commands import Option, SlashCommandGroup
import discord
from discord.ext import commands
from discord import guild
# from discord_slash import SlashCommand, SlashContext
# from discord_slash.utils.manage_commands import create_choice, create_option
import constants as CST

bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'))
#
#
# # slash = SlashCommand(bot, sync_commands=True)
#
# # name = 'getlastmessage',
# # description = "Get the last message of a text channel.",
# # guild_ids = 884913501968158720
# @bot.slash_command(description="Stuck? Use ME!")
# async def lol(ctx: discord.ApplicationContext):
#     """Get help about the most feature packed bot!!"""
#
#     await ctx.respond("embed=Help_Embed(), view=HelpOptions()")
#     message = await ctx.interaction.original_message()
#     await asyncio.sleep(5)
#     try:
#         await message.edit("This help session expired", embed=None, view=None)
#     except:
#         pass
#
# @bot.slash_command(description="prout Prout")
# async def prout(ctx: discord.ApplicationContext):
#     """Get help about the most feature packed bot!!"""
#
#     await ctx.respond("caca")
#
#
groupe = SlashCommandGroup(name="cat", description="Commands related to your ass")

@groupe.command(name="blab", description="bouh!")
async def tesin(ctx: discord.ApplicationContext):
    await ctx.respond("blabla")


@groupe.command(name="blabreponse", description="bouh 2!")
async def rep(ctx: discord.ApplicationContext, txt: Option(str, description="superu")):
    await ctx.respond(f"blabla : {txt}")


@bot.slash_command()
async def test(ctx):
    await ctx.send("hello")


@bot.slash_command(description="hello test")
async def tes(ctx: discord.ApplicationContext):
    await ctx.respond("coucou tes")


@bot.event
async def on_ready():
    print("ready")


bot.add_application_command(groupe)
pass
bot.run(CST.BOT_TOKEN)
