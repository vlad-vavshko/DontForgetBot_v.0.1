import telebot
from bot_files import config
from db import BotDB

from bot_files.markup import Markups
from bot_files.text_copies import Messages

markup = Markups()
msg = Messages()
BotDB = BotDB()
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    # check if user_id exists in DB and add if not
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(user_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name, username=message.from_user.username)
    welcome_sticker = open("stickers/welcome.webp", "rb")
    bot.send_sticker(message.chat.id, welcome_sticker)
    bot.send_message(message.from_user.id, msg.welcome_msg.format(
                         message.from_user.first_name, bot.get_me().first_name), parse_mode="html", reply_markup=markup.main, )

@bot.message_handler(content_types=['text'])
def start(message):
    print(message)


if __name__ == "__main__":
    bot.polling(none_stop=True)