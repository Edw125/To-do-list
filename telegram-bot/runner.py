import os
import time
import click as click

from aiogram.utils.executor import start_polling, set_webhook
from aiohttp import web
from loguru import logger
from handlers.handlers import register_handlers_client
from init_bot import setup_logging, set_commands, init_bot, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_PORT, WEBAPP_HOST


async def on_startup(dispatcher, url=None, cert=None):
    os.environ['TZ'] = 'Europe/Moscow'
    time.tzset()
    logger.info("Local time: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    await setup_logging(dispatcher)
    await set_commands(bot)
    if dispatcher["mode"] == "dev":
        await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    register_handlers_client(dispatcher)
    logger.info("Starting connection")


async def on_shutdown(dispatcher):
    if dispatcher["mode"] == "test":
        dispatcher.stop_polling()
    else:
        await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.storage.close()
    await dispatcher.wait_closed()
    logger.info("Closing connection")


@click.command()
@click.option('-m', '--mode', type=click.Choice(['test', 'dev'], case_sensitive=False), default="dev")
def main(mode):
    dp["mode"] = mode
    if mode == "test":
        logger.info("Enabled test mode")
        start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
    else:
        logger.info("Enabled dev mode")
        app["bot"] = bot
        app.update({"bot": bot})
        app.router.add_static(prefix="/static", path="static")
        set_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            web_app=app
        )
        web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
        logger.info(f"Service started on {WEBAPP_HOST}:{WEBAPP_PORT}")


if __name__ == '__main__':
    bot, dp, app = init_bot()
    main()
