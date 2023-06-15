import os
import sys

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand
from aiohttp import web
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = os.getenv("WEBAPP_HOST")
WEBAPP_PORT = os.getenv("WEBAPP_PORT")


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
    ]
    await bot.set_my_commands(commands)


def init_bot():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    app = web.Application()
    return bot, dp, app


async def setup_logging(dp):
    config = {
        "handlers": [
            {"sink": sys.stdout, "level": "INFO", "colorize": True, "enqueue": True},
            {"sink": "logs/bot.log", "level": "INFO", "rotation": "3 days", "enqueue": True}
        ],
    }
    logger.configure(**config)
    dp.middleware.setup(LoggingMiddleware())
