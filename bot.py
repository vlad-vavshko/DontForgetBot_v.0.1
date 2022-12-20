import telebot
from bot_files import config
from db import BotDB

from user import User
from bot_files.markup import Markups
from bot_files.text_copies import Messages

markup = Markups()
msg = Messages()
BotDB = BotDB()
bot = telebot.TeleBot(config.TOKEN)
user = User()

@bot.message_handler(commands=['start'])
def start(message):
    # check if user_id exists in DB and add if not
    print(BotDB.user_exists(message.from_user.id))
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(user_id=message.from_user.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name, username=message.from_user.username)
        print("user added to db")
    welcome_sticker = open("stickers/welcome.webp", "rb")
    bot.send_sticker(message.chat.id, welcome_sticker)
    bot.send_message(message.from_user.id, msg.welcome_msg.format(
                         message.from_user.first_name, bot.get_me().first_name), parse_mode="html", reply_markup=markup.main, )

@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, "Для додавання нового запису введіть наступні дані ⬇")
    msg = bot.send_message(message.chat.id, "👤 Ім'я:")
    bot.register_next_step_handler(msg, process_date_of_birth)

def process_date_of_birth(message):
    try:
        chat_id = message.chat.id
        user.user_name = message.text
        msg = bot.send_message(chat_id, "📅 Дата народження у форматі ДД.ММ.РРРР:")
        bot.register_next_step_handler(msg, process_add_complete)
    except Exception as e:
        bot.reply_to(message, "oops. Smth goes wrong 😵")
        print("process_date_of_birth: ", e)

def process_add_complete(message):
    chat_id = message.chat.id
    user.date_of_birth = message.text
    # result = "chat_id: {}, user_name: {}, date_of_birth: {}".format(chat_id, user_dict[chat_id].user_name, user_dict[chat_id].date_of_birth)
    # print(result)
    if user.date_of_birth_validation(message.text):
        user.age = user.get_age(message.text)
        user.zodiac_sign = user.get_zodiac_sign(message.text)
        complete_message = "✅ Новий запис додано до вашого списку!\n ➖➖➖➖➖➖➖➖➖➖ \n👤 Ім'я користувача: <b>{}</b> \n📅 Дата народження: <b>{}</b> \n🔢 Вік: <b>{}</b> \n💫 Знак зодіаку: <b>{}</b> \n ➖➖➖➖➖➖➖➖➖➖".format(user.user_name, user.date_of_birth, user.age, user.zodiac_sign)
        BotDB.add_record(user_id=chat_id, user_name=user.user_name, date_of_birth=user.date_of_birth)
        bot.send_message(chat_id, complete_message, reply_markup=markup.main, parse_mode="html")

    else:
        msg = bot.reply_to(message, "‼ Ви ввели неправильну дату народження! \n Спробуйте ще раз!.")
        bot.register_next_step_handler(msg, process_add_complete)



@bot.message_handler(content_types=['text'])
def handle_menu_commands(message):
    if message.chat.type == "private":
        if "Додати запис" in message.text:
            add(message)



if __name__ == "__main__":
    bot.polling(none_stop=True)