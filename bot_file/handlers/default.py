from aiogram import types
from random import randrange
from aiogram.dispatcher.filters import Text
from django.conf import settings
from ..loader import bot, dp
from ..keyboards import sign_inup_kb, admin_kb, default_kb
from ..models import TelegramUser
from .authorization import sign_in

HELP_TEXT = """
Привет 👋, я бот по продаже различных товаров! У нас есть такие команды как:

<b>Помощь ⭐️</b> - помощь по командам бота
<b>Описание 📌</> - адрес, контактные данные, график работы
<b>Каталог 🛒</b> - список товаров которые можно купить
<b>Админ 👑</b> - меню администратора

Но перед началом нужно <b>зарегистрироваться или войти</b> в свой профиль. 
Нажми на команду <b>Регистрация ✌️'</b> или <b>Войти 👋</b>
Если этого не сделаете, некоторые команды будут <b>не доступны</b> 🔴

Рады что вы используете данного бота ❤️
"""


# Сделан дефолтный хендлер
# @dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Привет ✋, я бот по продаже различных товаров!\n\n"
                                    "У меня вы можете купить все что захотите, чтобы увидеть список "
                                    "товаров которые у меня есть.\n\n"
                                    "Нажмите снизу на команду 'Каталог 🛒'\n\n"
                                    "Но для начала <b>нужно зарегистрироваться</b>, "
                                    "иначе остальные команды будут не доступны!\n\n"
                                    "Нажми на команду <b>Регистрация ✌️'</b> или <b>Войти 👋</b>",
                               reply_markup=sign_inup_kb.markup)
    except:
        await message.reply(text="Чтобы можно было общаться с ботом, "
                                 "ты можешь написать мне в личные сообщение: "
                                 "https://t.me/yourbot")


# @dp.message_handler(Text(equals='Помощь ⭐️'))
async def cmd_help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_TEXT, reply_markup=default_kb.markup)


# @dp.message_handler(Text(equals='Описание 📌'))
async def cmd_description(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Привет ✋, мы компания по продаже различных товаров!, "
                                "Мы очень рады что Вы используете"
                                "наш сервис ❤️, мы работает с Понедельника до "
                                "Пятницы.\n9:00 - 21:00")
    await bot.send_location(chat_id=message.chat.id,
                            latitude=randrange(1, 100),
                            longitude=randrange(1, 100))


# @dp.message_handler(Text(contains='Рассылка:'))
async def send_all(message: types.Message):
    if sign_in['current_state']:
        if message.chat.id == settings.ADMIN_ID:
            await message.answer(f"Сообщение: <b>{message.text[message.text.find(' '):]}</b> отправляется")
            async for user in TelegramUser.objects.filter(is_registered=True):
                await bot.send_message(chat_id=user.chat_id, text=message.text[message.text.find(' '):])
            await message.answer("Все успешно отправлено!")
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


# @dp.message_handler(Text(equals='Админ 👑'))
async def cmd_admin(message: types.Message):
    if sign_in['current_state']:
        if message.chat.id == settings.ADMIN_ID:
            await message.answer("Вы вошли в меню администратора 🤴\n\n"
                                 "Ниже предоставлены команды которые вы можете использовать 💭",
                                 reply_markup=admin_kb.markup)
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


# @dp.message_handler(Text(equals='Домой 🏠'))
async def cmd_home(message: types.Message):
    if sign_in['current_state']:
        if message.chat.id == settings.ADMIN_ID:
            await message.answer("Вы успешно перешли в главное меню!", reply_markup=default_kb.markup)
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


HELP_ADMIN_TEXT = '''
Привет администратор 🙋\n\n
На данный момент у тебя есть такие команды как:
- <b>Рассылка:</b> - благодаря этой команде ты можешь отправить сообщение всем пользователями данного бота.
Пример использования: Рассылка: 'ТЕКСТ РАССЫЛКИ'
'''


# @dp.message_handler(Text(equals='Помощь 🔔'))
async def cmd_help_admin(message: types.Message):
    if sign_in['current_state']:
        if message.chat.id == settings.ADMIN_ID:
            await message.answer(text=HELP_ADMIN_TEXT, reply_markup=admin_kb.markup)
        else:
            await message.answer("Вы не администратор, и вы не сможете отправлять рассылку!")
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


def default_handlers_register():
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_help, Text(equals='Помощь ⭐️'))
    dp.register_message_handler(cmd_description, Text(equals='Описание 📌'))
    dp.register_message_handler(send_all, Text(contains='Рассылка:'))
    dp.register_message_handler(cmd_admin, Text(equals='Админ 👑'))
    dp.register_message_handler(cmd_home, Text(equals='Домой 🏠'))
    dp.register_message_handler(cmd_help_admin, Text(equals='Помощь 🔔'))
