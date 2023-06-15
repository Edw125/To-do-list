import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers import keyboards
from handlers.endpoints import get_access_token
from states import Auth, Menu


async def start(message: types.Message):
    await message.answer(
        "Здравствуйте. Выберите действие",
        parse_mode="Markdown",
        reply_markup=await keyboards.kb_start()
    )


async def register(message: types.Message):
    pass


async def authorize_step_1(message: types.Message):
    await message.answer("Введите логин", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    await Auth.username.set()


async def authorize_step_2(message: types.Message, state: FSMContext):
    pattern = r"^[0-9A-Za-z-_]+$"
    if re.match(pattern, message.text) is None:
        await message.answer("Ошибка ввода. Логин содержит не поддерживающиеся символы")
        return
    await state.update_data(username=message.text)
    await message.answer("Введите пароль", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    await Auth.password.set()


async def authorize_step_3(message: types.Message, state: FSMContext):
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$"
    if re.match(pattern, message.text) is None:
        await message.answer("Ошибка ввода. Пароль должен содержать от 6 до 20 символов. "
                             "Должна быть хотя бы одна цифра, одна буква в нижнем регистре "
                             "и одна буква в верхнем регистре.")
        return
    await state.update_data(password=message.text)
    data = await state.get_data()
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
    await message.answer(
        "Успешно. Теперь можно выбрать действие",
        parse_mode="Markdown",
        reply_markup=await keyboards.kb_menu()
    )


async def menu(message: types.Message, state: FSMContext):
    pass


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
    dp.register_message_handler(authorize_step_1, Text(equals="Авторизоваться", ignore_case=True), state="*")
    dp.register_message_handler(authorize_step_2, state=Auth.username)
    dp.register_message_handler(authorize_step_3, state=Auth.password)
    dp.register_message_handler(menu, state=Menu.all_states)
