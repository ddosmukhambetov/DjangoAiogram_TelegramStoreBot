import re

from aiogram.dispatcher.filters import Text
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password, check_password
from ..loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from ..models import TelegramUser
from ..states import AuthState, SignInState, ForgotPasswordState
from ..keyboards import sign_inup_kb
from ..keyboards.registration_kb import markup, markup_cancel_forgot_password
from ..keyboards import default_kb


# Сделан хендлер авторизации
new_user = {}
sign_in = {'current_state': False}
update_data = {}

REGISTRATION_TEXT = """
Для регистрации сначала напишите свой логин!

Из чего должен состоять логин?
    - Логин должен состоять только из <b>латинских букв</b>!
    - Длинна логина должна быть <b>больше 3 символов(букв и цифр)</b>
    - Логин должен быть <b>уникальным и не повторяющимися</b>
    
Перед тем как отрпавить логин перепроверьте его!
"""


# @dp.message_handler(Text(equals='Отмена ❌', ignore_case=True), state='*')
async def command_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(text="Операция успешно отменена 🙅‍", reply_markup=sign_inup_kb.markup)


# @dp.message_handler(Text(equals='Регистрация ✌️'), state='*')
async def process_registration(message: types.Message):
    await message.answer(REGISTRATION_TEXT, reply_markup=markup)
    await AuthState.user_login.set()


# @dp.message_handler(state=AuthState.user_login)
async def process_login(message: types.Message, state: FSMContext):
    login = message.text
    if not await check_users_chat_id(chat_id=message.chat.id):
        if not await check_user(login=login):
            if re.match('^[A-Za-z]+$', login) and len(login) > 3:
                async with state.proxy() as data:
                    data['login'] = login
                    new_user['user_login'] = data['login']
                await message.answer("Теперь напиши пароль ✍️", reply_markup=markup)
                await AuthState.user_password.set()
            else:
                await message.answer("Логин должен состоять только из <b>латинских букв 🔡</b>\n\n"
                                     "Попробуйте еще раз ↩️!", reply_markup=markup)
                await AuthState.user_login.set()
        else:
            await message.answer("Пользователь с таким логином <b>уже есть</b>, попробуйте еще раз ↩️",
                                 reply_markup=markup)
            await AuthState.user_login.set()
    else:
        await message.answer("Пользователь с таким ID как у вас уже есть, войдите в свой аккаунт 🫡",
                             reply_markup=sign_inup_kb.markup)


# @dp.message_handler(state=AuthState.user_password)
async def process_password(message: types.Message, state: FSMContext):
    if len(message.text) > 5 and re.match('^[a-zA-Z0-9]+$', message.text) and \
            any(digit.isdigit() for digit in message.text):
        async with state.proxy() as data:
            data['password'] = message.text
        await message.answer("Введи пароль <b>еще раз</b> 🔄", reply_markup=markup)
        await AuthState.user_password_2.set()
    else:
        await message.answer("Пароль должен быть только из <b>латинских букв</b> "
                             "и содержать хотя бы <b>одну цифру</b>\n\n"
                             "Повторите попытку 🔄", reply_markup=markup)
        await AuthState.user_password.set()


# @dp.message_handler(state=AuthState.user_password_2)
async def process_password_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password_2'] = message.text
        new_user['user_password'] = data['password_2']
        if data['password'] == data['password_2']:
            new_user['chat_id'] = message.chat.id
            await save_user()
            await state.finish()
            await message.answer("Регистрация прошла <b>успешно</b> ✅\n\n"
                                 "Теперь, войдите в свой профиль 💝",
                                 reply_markup=sign_inup_kb.markup)
        else:
            await message.answer("Вы ввели пароль <b>не правильно</b> ❌\n\n"
                                 "Попробуйте еще раз 🔄", reply_markup=markup)
            await AuthState.user_password.set()


# @dp.message_handler(Text(equals='Войти 👋'))
async def command_sign_in(message: types.Message):
    await message.answer("Введите свой логин ✨", reply_markup=markup)
    await SignInState.login.set()


# @dp.message_handler(state=SignInState.login)
async def process_sign_in(message: types.Message, state: FSMContext):
    if await check_user(message.text):
        async with state.proxy() as sign_in_data:
            sign_in_data['login'] = message.text
            sign_in['login'] = sign_in_data['login']
        await message.answer("Теперь тебе нужно ввести пароль 🔐", reply_markup=markup_cancel_forgot_password)
        await SignInState.password.set()
    else:
        await message.answer("Такого логина <b>нет</b>, повторите еще раз ❌", reply_markup=markup)
        await SignInState.login.set()


# @dp.message_handler(state=SignInState.password)
async def process_pass(message: types.Message, state: FSMContext):
    async with state.proxy() as sign_in_data:
        sign_in_data['password'] = message.text
        sign_in['password'] = sign_in_data['password']
        sign_in['current_state'] = True
        if await get_password(username=sign_in['login'], password=sign_in['password']):
            await message.answer("Вход был <b>успешно</b> выполнен ⭐️", reply_markup=default_kb.markup)
            await state.finish()
        else:
            await message.answer("Пароль <b>не правильный</b> попробуйте еще раз 🔄",
                                 reply_markup=markup_cancel_forgot_password)
            await SignInState.password.set()


# @dp.message_handler(Text(equals='Забыли пароль? 🆘'), state='*')
async def forgot_password(message: types.Message):
    await message.answer("Чтобы изменить пароль, для начала введите логин 🫡", reply_markup=markup)
    await ForgotPasswordState.user_login.set()


# @dp.message_handler(state=ForgotPasswordState.user_login)
async def process_forgot_password_login(message: types.Message, state: FSMContext):
    if await check_login_chat_id(login=message.text, chat_id=message.chat.id):
        await message.answer("Логин <b>успешно</b> найден, "
                             "и ID пользователя совпадает с логином 🌟\n\n "
                             "Теперь вы <b>сможете</b> изменить пароль ✅\n\n"
                             "Введите <b>новый пароль</b> ✍️", reply_markup=markup)
        update_data['user_login'] = message.text
        await ForgotPasswordState.user_password.set()
    else:
        await message.answer("Вы <b>не прошли проверку</b> ❌\n\n"
                             "На это могут быть две причины:\n"
                             "1. Такого логина нет\n"
                             "2. Ваш ID пользователя не совпадает с логином который вы указали\n\n"
                             "Вы можете <b>повторить</b> попытку 🔄",
                             reply_markup=sign_inup_kb.markup)
        await state.finish()


# @dp.message_handler(state=ForgotPasswordState.user_password)
async def process_forgot_password_password(message: types.Message, state: FSMContext):
    if len(message.text) > 5 and re.match('^[a-zA-Z0-9]+$', message.text) and \
            any(digit.isdigit() for digit in message.text):
        async with state.proxy() as forgot_password_data:
            forgot_password_data['user_password'] = message.text
            update_data['user_password'] = forgot_password_data['user_password']
        await message.answer("Введи пароль <b>еще раз</b> 🔄", reply_markup=markup)
        await ForgotPasswordState.user_password_2.set()
    else:
        await message.answer("Пароль должен быть только из <b>латинских букв</b> "
                             "и содержать хотя бы <b>одну цифру</b>\n\n"
                             "Повторите попытку 🔄", reply_markup=markup)
        await ForgotPasswordState.user_password.set()


# @dp.message_handler(state=ForgotPasswordState.user_password_2)
async def process_forgot_password_password_2(message: types.Message, state: FSMContext):
    async with state.proxy() as forgot_password_data:
        forgot_password_data['user_password_2'] = message.text
        update_data['user_password'] = forgot_password_data['user_password_2']
        if forgot_password_data['user_password'] == forgot_password_data['user_password_2']:
            await update_user_password(login=update_data['user_login'], password=update_data['user_password'])
            await state.finish()
            await message.answer("Изменение пароля прошла <b>успешно</b> ✅\n\n"
                                 "Теперь, войдите в свой профиль 💝",
                                 reply_markup=sign_inup_kb.markup)
        else:
            await message.answer("Вы ввели пароль <b>не правильно</b> ❌\n\n"
                                 "Попробуйте еще раз 🔄", reply_markup=markup)
            await ForgotPasswordState.user_password.set()


@sync_to_async
def save_user():
    user = TelegramUser.objects.create(user_login=new_user['user_login'],
                                       user_password=make_password(new_user['user_password']),
                                       is_registered=True,
                                       chat_id=new_user['chat_id'])
    return user


@sync_to_async
def update_user_password(login, password):
    user = TelegramUser.objects.filter(user_login=login).update(user_password=make_password(password))
    return user


@sync_to_async
def get_password(username, password):
    user = TelegramUser.objects.get(user_login=username)
    if check_password(password, user.user_password):
        return True
    else:
        return False


@sync_to_async
def check_user(login):
    return TelegramUser.objects.filter(user_login=login).exists()


@sync_to_async
def check_login_chat_id(login, chat_id):
    return TelegramUser.objects.filter(user_login=login, chat_id=chat_id).exists()


@sync_to_async
def check_users_chat_id(chat_id):
    return TelegramUser.objects.filter(chat_id=chat_id).exists()


def authorization_handlers_register():
    dp.register_message_handler(command_cancel, Text(equals='Отмена ❌', ignore_case=True), state='*')
    dp.register_message_handler(process_registration, Text(equals='Регистрация ✌️'), state='*')
    dp.register_message_handler(process_login, state=AuthState.user_login)
    dp.register_message_handler(process_password, state=AuthState.user_password)
    dp.register_message_handler(process_password_2, state=AuthState.user_password_2)
    dp.register_message_handler(forgot_password, Text(equals='Забыли пароль? 🆘'), state='*')
    dp.register_message_handler(process_forgot_password_login, state=ForgotPasswordState.user_login)
    dp.register_message_handler(process_forgot_password_password, state=ForgotPasswordState.user_password)
    dp.register_message_handler(process_forgot_password_password_2, state=ForgotPasswordState.user_password_2)
    dp.register_message_handler(command_sign_in, Text(equals='Войти 👋'))
    dp.register_message_handler(process_sign_in, state=SignInState.login)
    dp.register_message_handler(process_pass, state=SignInState.password)
