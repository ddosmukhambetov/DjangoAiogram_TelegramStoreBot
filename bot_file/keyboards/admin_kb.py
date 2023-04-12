from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Реализована клавиатура админа
markup = ReplyKeyboardMarkup(resize_keyboard=True)
btn_1 = KeyboardButton("Домой 🏠")
btn_2 = KeyboardButton("Помощь 🔔")
markup.add(btn_1).add(btn_2)
