from aiogram.dispatcher.filters.state import StatesGroup, State


# Машина состояний для функции забыли пароль
class ForgotPasswordState(StatesGroup):
    user_login = State()
    user_password = State()
    user_password_2 = State()
