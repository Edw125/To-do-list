from aiogram import types


async def kb_start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    phone_button = types.KeyboardButton(
        text="Авторизоваться"
    )
    register_button = types.KeyboardButton(
        text="Зарегистрироваться"
    )
    keyboard.add(phone_button)
    keyboard.add(register_button)
    return keyboard


async def kb_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tasks = types.KeyboardButton(text="Получить список задач")
    keyboard.add(tasks)
    return keyboard
