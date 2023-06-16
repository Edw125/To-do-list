import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers import keyboards
from handlers.endpoints import get_access_token, get_task_list, check_user_register, update_user_data, \
    query_delete_task, query_create_task, query_update_task
from handlers.utils import parse_str
from states import Auth, Menu


async def start(message: types.Message):
    await message.answer(
        "Здравствуйте. Выберите действие",
        parse_mode="Markdown",
        reply_markup=await keyboards.kb_start()
    )


async def register(message: types.Message):
    pass


async def authorize_login_step_1(message: types.Message):
    await message.answer("Введите логин", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    await Auth.username.set()


async def authorize_login_step_2(message: types.Message, state: FSMContext):
    pattern = r"^[0-9A-Za-z-_]+$"
    if re.match(pattern, message.text) is None:
        await message.answer("Ошибка ввода. Логин содержит не поддерживающиеся символы")
        return
    await state.update_data(username=message.text)
    await message.answer("Введите пароль", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    await Auth.password.set()


async def authorize_login_step_3(message: types.Message, state: FSMContext):
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$"
    if re.match(pattern, message.text) is None:
        await message.answer("Ошибка ввода. Пароль должен содержать от 6 до 20 символов. "
                             "Должна быть хотя бы одна цифра, одна буква в нижнем регистре "
                             "и одна буква в верхнем регистре.")
        return
    await state.update_data(password=message.text)
    data = await state.get_data()
    data.update({"telegram_id": message.chat.id})
    result = await get_access_token(data)
    if not result:
        await message.answer(
            "Не удалось авторизоваться. Проверьте учетные данные и попробуйте снова",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_start()
        )
        await state.finish()
        return
    await Menu.jwt_token.set()
    await state.update_data(jwt_token=result.get("access"))
    await update_user_data(data, result.get("access"))
    await message.answer(
        "Успешно авторизован",
        parse_mode="Markdown",
        reply_markup=await keyboards.kb_menu()
    )


async def authorize_phone_step_1(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    telegram_id = message.chat.id
    response = await check_user_register({"phone": phone, "telegram_id": telegram_id})
    if response:
        await message.answer("Успешно авторизован", parse_mode="Markdown", reply_markup=await keyboards.kb_menu())
        await Menu.jwt_token.set()
        await state.update_data(jwt_token=response.get("access"))
        return
    await state.finish()
    await message.answer(
        "Пользователь не найден. Попробуйте войти по логину-паролю или зарегистрироваться",
        parse_mode="Markdown",
        reply_markup=await keyboards.kb_start()
    )


async def tasks(message: types.Message, state: FSMContext):
    data = await state.get_data()
    result = await get_task_list(data.get("jwt_token"))
    if result is not None:
        string = ""
        for task in result:
            string += f"id: {task.get('id')}, title: {task.get('title')[:50]}, " \
             f"desc: {task.get('description')[:100]}, status: {task.get('status')}\n"
        await message.answer(
            "Список задач: \n" + string,
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
    else:
        await message.answer(
            "Не удалось получить список задач",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_menu()
        )


async def delete_task(message: types.Message, state: FSMContext):
    if message.text == "Удалить":
        await Menu.delete_task.set()
        await message.answer(
            "Введите номер таска, который хотите удалить",
            parse_mode="Markdown",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return
    if not re.match(r"^[0-9]+$", message.text):
        await Menu.jwt_token.set()
        await message.answer(
            "Неправильный формат ввода",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
        return
    data = await state.get_data()
    jwt_token = data.get("jwt_token")
    result = await query_delete_task(message.text, jwt_token)
    if result:
        await message.answer(
            "Успешно удален",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
    else:
        await message.answer(
            "Удаление не удалось",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
    await Menu.jwt_token.set()


async def create_task(message: types.Message, state: FSMContext):
    if message.text == "Создать":
        await Menu.create_task.set()
        await message.answer(
            "Напишите заголовок (title) и описание (description) в таком формате: \n"
            "title: ... ; description: ... ",
            parse_mode="Markdown",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return
    parsed = parse_str(message.text)
    print(parsed)
    if not parsed:
        await Menu.jwt_token.set()
        await message.answer(
            "Неправильный формат ввода",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
        return
    data = await state.get_data()
    jwt_token = data.get("jwt_token")
    result = await query_create_task(parsed, jwt_token)
    if result:
        await message.answer(
            "Успешно создан",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
    else:
        await message.answer(
            "Создание не удалось",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
    await Menu.jwt_token.set()


async def update_task(message: types.Message, state: FSMContext):
    if message.text == "Обновить":
        await Menu.update_task.set()
        await message.answer(
            "Введите номер таска, напишите заголовок (title) и описание (description) в таком формате: \n"
            "id: 1 ; title: ... ; description: ... ; status: true",
            parse_mode="Markdown",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return
    parsed = parse_str(message.text)
    if not parsed:
        await Menu.jwt_token.set()
        await message.answer(
            "Неправильный формат ввода",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
        return
    data = await state.get_data()
    jwt_token = data.get("jwt_token")
    result = await query_update_task(parsed, jwt_token)
    if result:
        await message.answer(
            "Успешно обновлен",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
    else:
        await message.answer(
            "Обновление не удалось",
            parse_mode="Markdown",
            reply_markup=await keyboards.kb_edit()
        )
    await Menu.jwt_token.set()


async def logout(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Вы не в системе", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Вы успешно вышли из системы", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(logout, commands=["logout"], state="*")
    dp.register_message_handler(logout, Text(equals=["Выйти", "/logout"], ignore_case=True), state="*")
    dp.register_message_handler(authorize_phone_step_1,  content_types=types.ContentType.CONTACT, state="*")
    dp.register_message_handler(authorize_login_step_1, Text(equals="Авторизоваться по логину", ignore_case=True), state="*")
    dp.register_message_handler(authorize_login_step_2, state=Auth.username)
    dp.register_message_handler(authorize_login_step_3, state=Auth.password)
    dp.register_message_handler(tasks, Text(equals="Получить список задач", ignore_case=True), state=Menu.all_states)
    dp.register_message_handler(delete_task, Text(equals="Удалить", ignore_case=True), state=Menu.all_states)
    dp.register_message_handler(update_task, Text(equals="Обновить", ignore_case=True), state=Menu.all_states)
    dp.register_message_handler(create_task, Text(equals="Создать", ignore_case=True), state=Menu.all_states)
    dp.register_message_handler(delete_task, state=Menu.delete_task)
    dp.register_message_handler(update_task, state=Menu.update_task)
    dp.register_message_handler(create_task, state=Menu.create_task)
