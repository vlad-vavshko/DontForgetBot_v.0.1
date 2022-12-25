from telebot import types

class Markups:

    def __init__(self):
        # markups
        self.main = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        self.delete_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=12)
        self.confirm_action = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=6, one_time_keyboard=True)

        # buttons
        self.add_new_user_btn = types.KeyboardButton("📝 Додати запис")
        self.delete_user_btn = types.KeyboardButton("❌Видалити запис")
        self.get_all_users_info_btn = types.KeyboardButton("📖 Переглянути записи")

        self.confirm_btn = types.KeyboardButton("🗑 Так")
        self.decline_btn = types.KeyboardButton("⛔ Ні")


        # add buttons to marup
        self.main.add(self.add_new_user_btn, self.delete_user_btn, self.get_all_users_info_btn)
        self.confirm_action.add(self.confirm_btn, self.decline_btn)

    def generate_delete_markup(self, user_records):
        for name in user_records:
            button = types.KeyboardButton(text=name[0])
            self.delete_markup.add(button)

        # return self.delete_markup