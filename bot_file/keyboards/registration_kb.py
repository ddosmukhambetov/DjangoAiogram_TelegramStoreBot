from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_1 = KeyboardButton('Отмена ❌')

markup.add(btn_1)
