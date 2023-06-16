from aiogram import types


async def kb_start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    login_button = types.KeyboardButton(
        text="Авторизоваться по логину"
    )
    phone_button = types.KeyboardButton(
        text="Авторизоваться по телефону",
        request_contact=True
    )
    register_button = types.KeyboardButton(
        text="Зарегистрироваться"
    )

    keyboard.add(login_button)
    keyboard.add(phone_button)
    keyboard.add(register_button)
    return keyboard


async def kb_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tasks = types.KeyboardButton(text="Получить список задач")
    keyboard.add(tasks)
    return keyboard


async def kb_edit():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    delete_button = types.KeyboardButton(
        text="Удалить"
    )
    update_button = types.KeyboardButton(
        text="Обновить",
    )
    create_button = types.KeyboardButton(
        text="Создать",
    )
    tasks = types.KeyboardButton(text="Получить список задач")
    keyboard.add(delete_button)
    keyboard.add(update_button)
    keyboard.add(create_button)
    keyboard.add(tasks)
    return keyboard
