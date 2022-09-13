""" Database Manager """
import datetime

import disnake
import mysql.connector
from mysql.connector import Error


# Transformer ça en un objet ??
# l'init se fait à chaque requete


class DatabaseManager:
    def __init__(self, config):
        self.config = config
        # self.connector = self.init()

    def connect(self):
        try:
            cnx = mysql.connector.connect(
                host=self.config["DB_HOST"],
                port=self.config["DB_PORT"],
                db=self.config["DB_SCHEMA"],
                user=self.config["DB_USER"],
                passwd=self.config["DB_PASSWORD"],
                charset='utf8mb4',
                use_unicode=True,
                auth_plugin='mysql_native_password'
            )
            # print(f"Connected to database ({self.config['DB_HOST']}:{self.config['DB_PORT']})")
            return cnx
        except Exception as error:
            print("\nUnable to connect to database. Please check your credentials!\n" + str(error) + "\n")
            quit()

    def cursor(self):
        try:
            return self.connector.cursor(buffered=True)
        except Exception as e:
            print(f"\nAn error occurred while executing SQL statement\n{e}\n")
            quit()

    def create_table(self, stmt):
        database = teapot.managers.database.__init__()
        db = teapot.managers.database.db(database)

        db.execute(stmt)
        db.close()
        del db

    def insert(self, stmt, var):
        database = teapot.managers.database.__init__()
        db = teapot.managers.database.db(database)

        db.execute(stmt, var)
        database.commit()

        db.close()
        del db

    def insert_if_not_exists(self, stmt):
        database = teapot.managers.database.__init__()
        db = teapot.managers.database.db(database)

        db.execute(stmt)
        database.commit()

        db.close()
        del db

    def create_guild_table(self, guild):
        database = teapot.managers.database.__init__()
        db = teapot.managers.database.db(database)

        db.execute("SELECT * FROM `guilds` WHERE guild_id = '" + str(guild.id) + "'")
        if db.rowcount == 0:
            insert("INSERT INTO `guilds`(guild_id, guild_name) VALUES(%s, %s)", (guild.id, guild.name))

    def sql_commit(self, mysql_query, values):
        try:
            connection = self.connect()
            cursor = connection.cursor(buffered=True)
            cursor.execute(mysql_query, values)
            connection.commit()
        except mysql.connector.Error as error:
            print("Failed to execute MySQL query: {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def sql_query(self, mysql_query):
        try:
            connection = self.connect()
            cursor = connection.cursor(buffered=True)
            cursor.execute(mysql_query)
            return cursor.fetchall()
        except mysql.connector.Error as error:
            print("Failed to execute MySQL query: {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def log_db(self, bot):

        self.sql_commit(
            "INSERT INTO `guilds_logs`(timestamp,  result) VALUES(%s, %s)",
            [self.time(), "MEMBER_JOIN"])

        print(self.time())

    def add_guild(self, guild: disnake.Guild):
        result = self.sql_query("SELECT * FROM `guilds` WHERE guild_discord_id = '" + str(guild.id) + "'")
        if len(result) == 0:
            self.sql_commit("INSERT INTO `guilds`(guild_discord_id, name) VALUES(%s, %s)", (guild.id, guild.name))

    def add_user(self, user: disnake.Member):
        result = self.sql_query("SELECT * FROM `users` WHERE user_discord_id = '" + str(user.id) + "'")
        if len(result) == 0:
            self.sql_commit("INSERT INTO `users`(user_discord_id, name, discriminator, nickname) VALUES(%s, %s, %s, %s)",
                            (user.id, user.name, user.discriminator.zfill(4), user.nick))

        # try:
        #     connection = self.connect()
        #     cursor = connection.cursor(buffered=True)
        #     cursor.execute("SELECT * FROM `users` WHERE user_discord_id = '" + str(user.id) + "'")
        #     # result = cursor.fetchall()
        #     if cursor.rowcount == 0:
        #         cursor.execute("INSERT INTO `users`(user_discord_id, name, discriminator) VALUES(%s, %s, %s)",
        #                      (user.id, user.name, user.discriminator.zfill(4)))
        #         connection.commit()
        #
        # except mysql.connector.Error as error:
        #     print("Failed to execute MySQL query: {}".format(error))
        # finally:
        #     if connection.is_connected():
        #         cursor.close()
        #         connection.close()


    def time(self):
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

    def year(self):
        return str(datetime.datetime.now().year)
