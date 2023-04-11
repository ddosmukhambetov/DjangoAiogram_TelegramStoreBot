from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_1 = KeyboardButton('Отмена ❌')
markup.add(btn_1)


markup_cancel_forgot_password = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_1 = KeyboardButton('Отмена ❌')
btn_2 = KeyboardButton('Забыли пароль? 🆘')
markup_cancel_forgot_password.add(btn_1).add(btn_2)