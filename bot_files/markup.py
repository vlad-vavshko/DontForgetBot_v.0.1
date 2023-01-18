from telebot import types

class Markups:

    def __init__(self):
        # markups
        self.main = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        self.delete_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=12)
        self.dlt_confirm_action = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=6, one_time_keyboard=True)
        self.review_confirm_action = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=6, one_time_keyboard=True)

        # buttons
        self.add_new_user_btn = types.KeyboardButton("📝 Додати запис")
        self.delete_user_btn = types.KeyboardButton("❌Видалити запис")
        self.get_all_users_info_btn = types.KeyboardButton("📖 Переглянути записи")

        self.dlt_confirm_btn = types.KeyboardButton("🗑 Так")
        self.dlt_decline_btn = types.KeyboardButton("⛔ Ні")

        self.review_confirm_btn = types.KeyboardButton("Так")
        self.review_decline_btn = types.KeyboardButton("Ні")




        # add buttons to markup
        self.main.add(self.add_new_user_btn, self.delete_user_btn, self.get_all_users_info_btn)
        self.dlt_confirm_action.add(self.dlt_confirm_btn, self.dlt_decline_btn)
        self.review_confirm_action.add(self.review_confirm_btn, self.review_decline_btn)


    def generate_delete_markup(self, user_records):
        for name in user_records:
            button = types.KeyboardButton(text=name[0])
            self.delete_markup.add(button)

        # return self.delete_markup