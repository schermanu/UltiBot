import json

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Context

import samples
from samples import exceptions
from samples import TheBot

def __init__(bot: commands.Bot):
    """ Initialize events """
    member_join(bot)
    # member_leave(bot)
    guild_join(bot)
    message_send(bot)
    # message_edit(bot)
    # message_delete(bot)
    command_error(bot)


def member_join(bot: TheBot):
    @bot.event
    async def on_member_join(member):
        bot.db.add_user(member)

        # bot.db.sql_commit(
        #             "INSERT INTO `guilds_logs`(timestamp, guild_id, channel_id, user_id, type) VALUES(%s, %s, %s, %s, %s)",
        #             (bot.db.time(), member.guild.id, member.channel.id, member.id, "MEMBER_JOIN"))



def member_leave(bot: TheBot):
    @bot.event
    async def on_member_remove(member):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute(
                    "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s)",
                    (teapot.time(), member.guild.id, member.channel.id, member.id, "MEMBER_REMOVE"))
                database.commit()
            except Exception as e:
                print(e)


def guild_join(bot: TheBot):
    @bot.event
    async def on_guild_join(ctx):
        bot.db.add_guild(ctx)
        # if teapot.config.storage_type() == "mysql":
        #     teapot.database.create_guild_table(ctx.guild)


def message_send(bot):
    @bot.event
    async def on_message(message: disnake.Message):
        bot.db.add_user(message.author)
        #
        # if teapot.config.storage_type() == "mysql":
        #     try:
        #         database = teapot.database.__init__()
        #         db = teapot.database.db(database)
        #         db.execute("SELECT * FROM `users` WHERE user_id = '" + str(message.author.id) + "'")
        #         if db.rowcount == 0:
        #             db.execute("INSERT INTO `users`(user_id, user_name, user_discriminator) VALUES(%s, %s, %s)",
        #                        (message.author.id, message.author.name, message.author.discriminator.zfill(4)))
        #             database.commit()
        #
        #         db.execute("SELECT * FROM `channels` WHERE channel_id = '" + str(message.channel.id) + "'")
        #         if db.rowcount == 0:
        #             db.execute("INSERT INTO `channels`(channel_id, channel_name) VALUES(%s, %s)",
        #                        (message.channel.id, message.channel.name))
        #             database.commit()
        #         db.execute(
        #             "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, message_id, user_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s, %s)",
        #             (teapot.time(), message.guild.id, message.channel.id, message.id, message.author.id,
        #              "MESSAGE_SEND", message.content))
        #         database.commit()
        #     except Exception as e:
        #         print(e)
        # await bot.process_commands(message)

    # @bot.event
    # async def on_message(message):
    #     # SAO Easter Egg
    #     punctuations = '!()-[]{};:\'"\\,<>./?@#$%^&*_~'
    #     # remove punctuation from the string
    #     msg = ""
    #     for char in message.content.lower():
    #         if char not in punctuations:
    #             msg = msg + char
    #
    #     # profanity check
    #     prob = predict_prob([msg])
    #     if prob >= 0.8:
    #         em = discord.Embed(title=f"AI Analysis Results", color=0xC54B4F)
    #         em.add_field(name='PROFANITY DETECTED! ', value=str(prob[0]))
    #         await message.channel.send(embed=em)
    #
    #     if msg.startswith("system call "):
    #         content = msg[12:].split(" ")
    #         if content[0].lower() == "inspect":
    #             if content[1].lower() == "entire":
    #                 if content[2].lower() == "command":
    #                     if content[3].lower() == "list":
    #                         em = discord.Embed(title=f"🍢 SAO Command List", color=0x7400FF)
    #                         em.set_thumbnail(
    #                             url="https://cdn.discordapp.com/attachments/668816286784159763/674285661510959105/Kirito-Sao-Logo-1506655414__76221.1550241566.png")
    #                         em.add_field(name='Commands',
    #                                      value="generate xx element\ngenerate xx element xx shape\ninspect entire command list")
    #
    #                         em.set_footer(text=f"{teapot.copyright()} | Code licensed under the MIT License")
    #                         await message.channel.send(embed=em)
    #         elif content[0].lower() == "generate":
    #             if content[-1].lower() == "element":
    #                 em = discord.Embed(title=f"✏ Generated {content[1].lower()} element!",
    #                                    color=0xFF0000)
    #                 await message.channel.send(embed=em)
    #             if content[-1].lower() == "shape":
    #                 if content[2].lower() == "element":
    #                     em = discord.Embed(
    #                         title=f"✏ Generated {content[-2].lower()} shaped {content[1].lower()} element!",
    #                         color=0xFF0000)
    #                     await message.channel.send(embed=em)
    #     await bot.process_commands(message)


def message_edit(bot):
    @bot.event
    async def on_raw_message_edit(ctx):
        guild_id = json.loads(json.dumps(ctx.data))['guild_id']
        channel_id = json.loads(json.dumps(ctx.data))['channel_id']
        message_id = json.loads(json.dumps(ctx.data))['id']
        try:
            author_id = json.loads(json.dumps(json.loads(json.dumps(ctx.data))['author']))['id']
            content = json.loads(json.dumps(ctx.data))['content']
            if teapot.config.storage_type() == "mysql":
                try:
                    database = teapot.database.__init__()
                    db = teapot.database.db(database)
                    db.execute(
                        "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, message_id, user_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                        (teapot.time(), guild_id, channel_id, message_id, author_id, "MESSAGE_EDIT", content))
                    database.commit()
                except Exception as e:
                    print(e)
        except:
            content = str(json.loads(json.dumps(ctx.data))['embeds'])
            if teapot.config.storage_type() == "mysql":
                try:
                    database = teapot.database.__init__()
                    db = teapot.database.db(database)
                    db.execute(
                        "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, message_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s)",
                        (teapot.time(), guild_id, channel_id, message_id, "MESSAGE_EDIT", content))
                    database.commit()
                except Exception as e:
                    print(e)


def message_delete(bot):
    @bot.event
    async def on_message_delete(ctx):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute(
                    "INSERT INTO `guild_logs`(timestamp, guild_id, channel_id, message_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s, %s)",
                    (teapot.time(), ctx.guild.id, ctx.channel.id, ctx.id, ctx.author.id, "MESSAGE_DELETE"))
                database.commit()
            except Exception as e:
                print(e)


def command_error(bot):
    @bot.event
    async def on_command_error(ctx, e):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute(
                    "INSERT INTO `bot_logs`(timestamp, type, class, message) VALUES(%s, %s, %s, %s)",
                    (teapot.time(), "CMD_ERROR", __name__, str(e)))
                database.commit()
            except Exception as e:
                print(e)

    @bot.event
    async def on_command_error(context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error
        :param context: The normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = disnake.Embed(
                title="Hey, please slow down!",
                description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(
                title="Error!",
                description="You are missing the permission(s) `" + ", ".join(
                    error.missing_permissions) + "` to execute this command!",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        elif isinstance(error, exceptions.UserBlacklisted):
            """
            The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
            the @checks.is_owner() check in your command, or you can raise the error by yourself.

            'hidden=True' will make so that only the user who execute the command can see the message
            """
            embed = disnake.Embed(
                title="Error!",
                description="You are blacklisted from using the bot.",
                color=0xE02B2B
            )
            print("A blacklisted user tried to execute a command.")
            # return await context.send(embed=embed) #embec visible by everyone which is not good
            return
        elif isinstance(error, exceptions.UserNotOwner):
            """
            The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
            the @checks.is_owner() check in your command, or you can raise the error by yourself.

            'hidden=True' will make so that only the user who execute the command can see the message
            """
            embed = disnake.Embed(
                title="Error!",
                description="You are blacklisted from using the bot.",
                color=0xE02B2B
            )
            print("A user tried to execute an owner command.")
            # return await context.send(embed=embed) #embec visible by everyone which is not good
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = disnake.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code.
                description=str(error).capitalize(),
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        elif isinstance(error, commands.CommandNotFound):
            embed = disnake.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code.
                description=str(error).capitalize(),
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        raise error


def message(bot):
    @bot.event
    async def on_message(msg: disnake.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix
        :param msg: The message that was sent.
        """
        if msg.author == bot.user or msg.author.bot:
            return
        await bot.process_commands(msg)


def slash_command(bot):
    @bot.event
    async def on_slash_command(interaction: ApplicationCommandInteraction) -> None:
        """
        The code in this event is executed every time a slash command has been *successfully* executed
        :param interaction: The slash command that has been executed.
        """
        print(
            f"Executed {interaction.data.name} command in {interaction.guild.name} (ID: {interaction.guild.id}) by {interaction.author} (ID: {interaction.author.id})")


def slash_command_error(bot):
    @bot.event
    async def on_slash_command_error(interaction: ApplicationCommandInteraction, error: Exception) -> None:
        """
        The code in this event is executed every time a valid slash command catches an error
        :param interaction: The slash command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, exceptions.UserBlacklisted):
            """
            The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
            the @checks.is_owner() check in your command, or you can raise the error by yourself.
    
            'hidden=True' will make so that only the user who execute the command can see the message
            """
            embed = disnake.Embed(
                title="Error!",
                description="You are blacklisted from using the bot.",
                color=0xE02B2B
            )
            print("A blacklisted user tried to execute a command.")
            return await interaction.send(embed=embed, ephemeral=True)
        elif isinstance(error, exceptions.UserNotOwner):
            """
            The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
            the @checks.is_owner() check in your command, or you can raise the error by yourself.
    
            'hidden=True' will make so that only the user who execute the command can see the message
            """
            embed = disnake.Embed(
                title="Error!",
                description="You are not owner of the bot.",
                color=0xE02B2B
            )
            print("A user tried to execute an owner command.")
            return await interaction.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = disnake.Embed(
                title="Error!",
                description="You are missing the permission(s) `" + ", ".join(
                    error.missing_permissions) + "` to execute this command!",
                color=0xE02B2B
            )
            print("A blacklisted user tried to execute a command.")
            return await interaction.send(embed=embed, ephemeral=True)
        raise error


def command_completion(bot):
    @bot.event
    async def on_command_completion(context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed
        :param context: The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        print(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.message.guild.id}) by {context.message.author} (ID: {context.message.author.id})")
