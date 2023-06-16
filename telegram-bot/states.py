from aiogram.dispatcher.filters.state import State, StatesGroup


class Auth(StatesGroup):
    username = State()
    password = State()


class Menu(StatesGroup):
    jwt_token = State()
    delete_task = State()
    update_task = State()
    create_task = State()
