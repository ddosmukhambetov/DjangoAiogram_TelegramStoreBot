from aiogram.dispatcher.filters.state import StatesGroup, State


# Машина состояний для регистрации
class AuthState(StatesGroup):
    user_login = State()
    user_password = State()
    user_password_2 = State()
