from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btn_1 = KeyboardButton('/start')
btn_2 = KeyboardButton('/help')
btn_3 = KeyboardButton('/description')
btn_4 = KeyboardButton('/catalog')
markup.add(btn_1).insert(btn_2).add(btn_3).insert(btn_4)
