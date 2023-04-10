from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

btn_1 = KeyboardButton('Регистрация ✌️')
btn_2 = KeyboardButton('Войти 👋')
btn_3 = KeyboardButton('Забыли пароль? 🆘')

markup.add(btn_1).insert(btn_2).add(btn_3)
