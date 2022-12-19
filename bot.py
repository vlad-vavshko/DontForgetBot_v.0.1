import telebot
from bot_files import config
from db import BotDB

from bot_files.text_copies import Messages

msg = Messages()
BotDB = BotDB()
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    print(BotDB.user_exists(message.from_user.id))
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(user_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name, username=message.from_user.username)
        print('user added')
    bot.send_message(message.from_user.id, msg.welcome_msg.format(
                         message.from_user.first_name, bot.get_me().first_name), parse_mode="html")


@bot.message_handler(content_types=['text'])
def start(message):
    print(message)


if __name__ == "__main__":
    bot.polling(none_stop=True)