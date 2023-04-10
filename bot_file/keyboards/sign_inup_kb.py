from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

btn_1 = KeyboardButton('Регистрация ✌️')
btn_2 = KeyboardButton('Войти 👋')

markup.add(btn_1).add(btn_2)
