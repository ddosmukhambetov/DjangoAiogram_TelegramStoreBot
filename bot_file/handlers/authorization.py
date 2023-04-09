from aiogram.dispatcher.filters import Text
from asgiref.sync import sync_to_async

from ..loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

from ..models import TelegramUser
from ..states import AuthState

new_user = {}


REGISTRATION_TEXT = """
Для регистрации сначала напишите свой логин!

Из чего должен состоять логин?
    - Логин должен состоять только из <b>латинских букв</b> и <b>цифр</b>!
    - Длинна логина должна быть <b>больше 3 символов(букв и цифр)</b>
    - Логин должен быть <b>уникальным и не повторяющимися</b>
    
Перед тем как отрпавить логин перепроверьте его!
"""


@dp.message_handler(Text(equals='Регистрация'), state='*')
async def process_registration(message: types.Message):
    new_user['chat_id'] = message.chat.id
    await message.answer(REGISTRATION_TEXT)
    await AuthState.user_login.set()


# @dp.message_handler(state=AuthState.user_login)
async def process_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
        new_user['user_login'] = data['login']
    await message.answer("Теперь напиши пароль!")
    await AuthState.user_password.set()


# @dp.message_handler(state=AuthState.user_password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await message.answer("Введи пароль еще раз")
    await AuthState.user_password_2.set()


# @dp.message_handler(state=AuthState.user_password_2)
async def process_password_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password_2'] = message.text
        new_user['user_password'] = data['password_2']
        if data['password'] == data['password_2']:
            await message.answer("Регистрация прошла успешно!")
            await save_user()
        else:
            await message.answer("Вы ввели пароль не правильно!")
            await AuthState.user_password.set()


@sync_to_async
def save_user():
    user = TelegramUser.objects.create(user_login=new_user['user_login'],
                                       user_password=new_user['user_password'],
                                       is_registered=True)
    return user


def authorization_handlers_register():
    dp.register_message_handler(process_registration, Text(equals='Регистрация'), state='*')
    dp.register_message_handler(process_login, state=AuthState.user_login)
    dp.register_message_handler(process_password, state=AuthState.user_password)
    dp.register_message_handler(process_password_2, state=AuthState.user_password_2)
