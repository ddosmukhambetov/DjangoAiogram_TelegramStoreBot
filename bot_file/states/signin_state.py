from aiogram.dispatcher.filters.state import StatesGroup, State


class SignInState(StatesGroup):
    login = State()
    password = State()
