import datetime
from datetime import date
import re
import months

class User:
    def __init__(self):
        self.user_name = None
        self.date_of_birth = None
        self.age = None
        self.zodiac_sign = None

    def date_of_birth_validation(self, birthdate):
        try:
            match = re.match(
                r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{4})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{4})$',
                birthdate)
            day_of_birth = datetime.datetime.strptime(birthdate, '%d.%m.%Y').date()
            today = date.today()
            if match != None and (day_of_birth <= today) is True:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def get_age(self,birthdate):
        today = date.today()
        day_of_birth = datetime.datetime.strptime(birthdate, '%d.%m.%Y').date()

        year = today.year - day_of_birth.year
        if today.month >= day_of_birth.month:
            month = today.month - day_of_birth.month
        else:
            year = year - 1
            month = 12 + today.month - day_of_birth.month

        if today.day >= day_of_birth.day:
            day = today.day - day_of_birth.day
        else:
            month = month - 1
            if month < 0:
                month = 11
                year = year - 1
            days_in_month = months.Month(year, month).n_days - 2
            day = days_in_month + today.day - day_of_birth.day

        return f"{year}р. {month}м. {day}д."

    def get_zodiac_sign(self, birthdate):
        day = int(birthdate.split('.')[0])
        month = int(birthdate.split('.')[1])
        astro_sign = None
        match month:
            case 12:
                if day < 22:
                    astro_sign = "♐ Стрілець"
                else:
                    astro_sign = "♑ Козеріг"
            case 1:
                if day < 20:
                    astro_sign = "♑ Козеріг"
                else:
                    astro_sign = "♒ Водолій"
            case 2:
                if day < 19:
                    astro_sign = "♒ Водолій"
                else:
                    astro_sign = "♓ Риби"
            case 3:
                if day < 21:
                    astro_sign = "♓ Риби"
                else:
                    astro_sign = "♈ Овен"
            case 4:
                if day < 20:
                    astro_sign = "♈ Овен"
                else:
                    astro_sign = "♉ Телець"
            case 5:
                if day < 21:
                    astro_sign = "♉ Телець"
                else:
                    astro_sign = "♊ Близнюки"
            case 6:
                if day < 21:
                    astro_sign = "♊ Близнюки"
                else:
                    astro_sign = "♋ Рак"
            case 7:
                if day < 23:
                    astro_sign = "♋ Рак"
                else:
                    astro_sign = "♌ Лев"
            case 8:
                if day < 23:
                    astro_sign = "♌ Лев"
                else:
                    astro_sign = "♍ Діва"
            case 9:
                if day < 23:
                    astro_sign = "♍ Діва"
                else:
                    astro_sign = "♎ Терези"
            case 10:
                if day < 23:
                    astro_sign = "♎ Терези"
                else:
                    astro_sign = "♏ Скорпіон"
            case 11:
                if day < 22:
                    astro_sign = "♏ Скорпіон"
                else:
                    astro_sign = "♐ Стрілець"

        return astro_sign


    def check_user_name_exists(self, searching_user, user_records):
        for name in user_records:
            if searching_user.lower() == name[0].lower():
                return True
        return False