
from aiogram import Dispatcher, types

from handlers import keyboards


async def start(message: types.Message):
    await message.answer(
        "Здравствуйте. Выберите действие",
        parse_mode="Markdown",
        reply_markup=await keyboards.kb_start()
    )


async def register(message: types.Message):
    pass


async def authorize(message: types.Message):
    pass
