import telebot
from bot_files import config
from db import BotDB
from telebot import types

from user import User
from bot_files.markup import Markups
from bot_files.text_copies import Messages

markup = Markups()
BotDB = BotDB()
bot = telebot.TeleBot(config.TOKEN)
user = User()

@bot.message_handler(commands=['start'])
def start(message):
    # check if user_id exists in DB and add if not
    msg = Messages()
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
        user_records = BotDB.get_user_records(chat_id)
        if (user.check_user_name_exists(searching_user=user.user_name, user_records=user_records)):
            msg = bot.reply_to(message, "Запис з таким ім'ям уже існує, будь ласка введть інше")
            bot.register_next_step_handler(msg, process_date_of_birth)
        else:
            msg = bot.send_message(chat_id, "📅 Дата народження у форматі ДД.ММ.РРРР:")
            bot.register_next_step_handler(msg, process_add_complete)
    except Exception as e:
        bot.reply_to(message, "Щось пішло не так, спробуйте будь ласка пізніше  😵‍")
        print("process_date_of_birth: ", e)

def process_add_complete(message):
    try:
        chat_id = message.chat.id
        user.date_of_birth = message.text
        msg = Messages()
        if user.date_of_birth_validation(message.text):
            user.age = user.get_age(message.text)
            user.zodiac_sign = user.get_zodiac_sign(message.text)
            complete_message = msg.add_complete_msg.format(user.user_name, user.date_of_birth, user.age, user.zodiac_sign)
            BotDB.add_record(user_id=chat_id, user_name=user.user_name, date_of_birth=user.date_of_birth)
            bot.send_message(chat_id, complete_message, reply_markup=markup.main, parse_mode="html")

        else:
            msg = bot.reply_to(message, "‼ Ви ввели неправильну дату народження! \nСпробуйте ще раз 😉")
            bot.register_next_step_handler(msg, process_add_complete)
    except Exception as e:
        bot.reply_to(message, "Щось пішло не так, спробуйте будь ласка пізніше  😵‍")
        print("process_add_complete: ", e)

@bot.message_handler(commands=['delete'])
def delete(message):
    try:
        msg = Messages()
        user_records = BotDB.get_user_records(message.chat.id)
        if len(user_records) > 0:
            # generate markup
            delete_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=12)
            for name in user_records:
                button = types.KeyboardButton(text=name[0])
                delete_markup.add(button)

            msg = bot.send_message(message.chat.id, "Який запис бажаєте видалити?", reply_markup=delete_markup)
            bot.register_next_step_handler(msg, delete_check_if_name_exists, delete_markup)
        else:
            bot.send_message(message.chat.id, msg.nothing_to_delete_msg, reply_markup=markup.main)
    except Exception as e:
        bot.reply_to(message, "Щось пішло не так, спробуйте будь ласка пізніше  😵‍")
        print("delete: ", e)

def delete_check_if_name_exists(message, delete_markup):
    try:
        msg = Messages()
        user_to_delete = message.text
        user_records = BotDB.get_user_records(message.chat.id)
        if(user.check_user_name_exists(searching_user=user_to_delete, user_records=user_records)):
            next_step_msg = bot.send_message(message.chat.id, msg.confirm_delete.format(user_to_delete), parse_mode="html", reply_markup=markup.dlt_confirm_action)
            bot.register_next_step_handler(next_step_msg, complete_delete, user_to_delete)
        else:
            reply = bot.reply_to(message, "Такого запису не знайдено, спробуйте ще раз!", reply_markup=types.ReplyKeyboardRemove(selective=False))
            bot.send_message(message.chat.id, "Який запис бажаєте видалити?", reply_markup=delete_markup)
            bot.register_next_step_handler(reply, delete_check_if_name_exists, delete_markup)
    except Exception as e:
        bot.reply_to(message, "Щось пішло не так, спробуйте будь ласка пізніше  😵‍")
        print("check_if_name_exists: ", e)
def complete_delete(message, user_to_delete):
    try:
        msg = Messages()
        user_answer = message.text
        if "так" in user_answer.lower():
            if BotDB.delete_user_record(user_id=message.chat.id, user_name=user_to_delete) == None:
                bot.send_message(message.chat.id, msg.delete_success.format(user_to_delete), reply_markup=markup.main, parse_mode="html")
        elif "ні" in user_answer.lower():
            bot.send_message(message.chat.id,"Скасування... 🚫", reply_markup=markup.main)
        else:
            bot.register_next_step_handler(bot.reply_to(message, "Не зрозумів Вашу відповідь 🤔", reply_markup=markup.dlt_confirm_action), complete_delete, user_to_delete)
    except Exception as e:
        bot.reply_to(message, "Щось пішло не так, спробуйте будь ласка пізніше  😵‍")
        print(e)

@bot.message_handler(commands=['review'])
def review(message):
    try:
        #check if user has records
        msg =Messages()
        user_records = BotDB.get_user_records(user_id=message.chat.id)
        if len(user_records) > 0:
            # generate markup
            user_records_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=12, one_time_keyboard=True)
            user_records_markup.add(types.KeyboardButton(text="Усі записи"))
            for name in user_records:
                button = types.KeyboardButton(text=name[0])
                user_records_markup.add(button)

            next_step_msg = bot.send_message(message.chat.id, "Який запис бажаєте переглянути?", reply_markup=user_records_markup)
            bot.register_next_step_handler(next_step_msg, review_check_if_name_exists, user_records_markup)
        else:
            bot.send_message(message.chat.id, msg.nothing_to_review_msg, reply_markup=markup.main)
    except Exception as e:
        bot.reply_to(message, "Щось пішло не так, спробуйте будь ласка пізніше  😵‍")
        print("review: ", e)

def review_check_if_name_exists(message, user_records_markup):
    try:
        user = User()
        user_records = BotDB.get_all_records_details(message.chat.id)
        msg = Messages()
        if message.text.lower() == "усі записи":
            output = ""
            for record in user_records:
                user.user_name = record[0]
                user.date_of_birth = record[1]
                user.age = user.get_age(user.date_of_birth)
                user.zodiac_sign = user.get_zodiac_sign(user.date_of_birth)
                bot.send_message(message.chat.id, msg.review_complete_msg.format(user.user_name, user.date_of_birth, user.age,
                                                           user.zodiac_sign), parse_mode="html")
            bot.send_message(message.chat.id, "✅ Усі записи виведено", reply_markup=markup.main)
        else:
            msg = Messages()
            user_to_review = message.text
            if (user.check_user_name_exists(searching_user=user_to_review, user_records=user_records)):
                next_step_msg = bot.send_message(message.chat.id, msg.selected_for_review.format(user_to_review), parse_mode="html", reply_markup= markup.review_confirm_action)
                bot.register_next_step_handler(next_step_msg, complete_review, user_to_review)
            else:
                reply = bot.reply_to(message, "Такого запису не знайдено, спробуйте ще раз!",
                                     reply_markup=types.ReplyKeyboardRemove(selective=False))
                bot.send_message(message.chat.id, "Який запис бажаєте переглянути?", reply_markup=user_records_markup)
                bot.register_next_step_handler(reply, review_check_if_name_exists, user_records_markup)
    except Exception as e:
        bot.reply_to("Щось пішло не так, спробуйте будь ласка пізніше  😵‍")
        print("review_check_if_name_exists: ", e)

def complete_review(message, user_to_review):
    try:
        msg = Messages()
        user_answer = message.text
        user_id = message.chat.id
        if "так" in user_answer.lower():
            user = User()
            user_record_db = BotDB.get_record_details(user_id, user_to_review)
            user.user_name = user_to_review
            user.date_of_birth = user_record_db[0][1]
            user.age = user.get_age(user.date_of_birth)
            user.zodiac_sign = user.get_zodiac_sign(user.date_of_birth)
            complete_message = msg.review_complete_msg.format(user.user_name, user.date_of_birth, user.age,
                                                           user.zodiac_sign)
            bot.send_message(user_id, complete_message, parse_mode="html", reply_markup=markup.main)
        elif "ні" in user_answer.lower():
            bot.send_message(message.chat.id, "Скасування... 🚫", reply_markup=markup.main)
        else:
            bot.register_next_step_handler(
                bot.reply_to(message, "Не зрозумів Вашу відповідь 🤔", reply_markup=markup.review_confirm_action),
                complete_delete, user_to_review)




    except Exception as e:
        bot.reply_to(message, "Щось пішло не так, спробуйте будь ласка пізніше  😵‍")
        print(e)



@bot.message_handler(content_types=['text'])
def handle_menu_commands(message):
    if message.chat.type == "private":
        if "Додати запис" in message.text:
            add(message)
        elif "Видалити запис" in message.text:
            delete(message)
        elif "Переглянути записи" in message.text:
            review(message)



if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)