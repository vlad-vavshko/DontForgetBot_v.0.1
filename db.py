import sqlite3

class BotDB:

    # def __init__(self):
    #     # init DB connection
    #     self.connection = sqlite3.connect('users.db')
    #     self.cursor = self.connection.cursor()
    db_name = 'bot_users.db'
    def user_exists(self, user_id, ):
        # Check if user exists in DB
        self.connection = sqlite3.connect('bot_users.db')
        self.cursor = self.connection.cursor()
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = (?)", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        # get id of user based on user_id from Telegram
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = (?)", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, first_name, last_name, username):
        # add user to the DB
        self.cursor.execute("INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `tg_username`) VALUES (?, ?, ?, ?)", (user_id, first_name, last_name, username))
        return self.connection.commit()

    def add_record(self, user_id, user_name, date_of_birth):
        self.connection = sqlite3.connect('bot_users.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("INSERT INTO `user_records` (`user_id`, `user_name`, `date_of_birth`) VALUES (?, ?, ?)", (user_id, user_name, date_of_birth))
        return self.connection.commit()

    def get_user_records(self, user_id):
        self.connection = sqlite3.connect('bot_users.db')
        self.cursor = self.connection.cursor()
        result = self.cursor.execute("SELECT `user_name` FROM `user_records` WHERE `user_id` = (?)", (user_id,))
        return result.fetchall()


    def close(self):
        # close DB connection
        self.connection.close()
