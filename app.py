# tg_bot_dev/app.py
import asyncio
import logging

from aiogram import Bot, Dispatcher
from .handlers import zabbix_handler_router
from .settings import settings  # <-- импортируем готовые настройки

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(name)s: %(message)s",
)

bot = Bot(token=settings.token)
dp = Dispatcher()

async def main():
    dp.include_router(zabbix_handler_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
