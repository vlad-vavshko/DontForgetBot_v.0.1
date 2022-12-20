from telebot import types

class Markups:

    def __init__(self):
        # markups
        self.main = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        # buttons
        self.add_new_user_btn = types.KeyboardButton("📝 Додати запис")
        self.delete_user_btn = types.KeyboardButton("❌Видалити запис")
        self.get_all_users_info_btn = types.KeyboardButton("📖 Переглянути записи")




        # add buttons to marup
        self.main.add(self.add_new_user_btn, self.delete_user_btn, self.get_all_users_info_btn)
