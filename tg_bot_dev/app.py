# tg_bot_dev/app.py
import asyncio
import logging
from aiogram import Bot, Dispatcher

from tg_bot_dev.handlers import zabbix_handler_router   # абсолютный импорт надёжнее при запуске -m
from tg_bot_dev.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(name)s: %(message)s",
)

async def main():
    # Создаём инстансы внутри main (чтобы можно было использовать await перед стартом)
    bot = Bot(token=settings.token)  # проверь: поле называется token?
    dp = Dispatcher()

    # ✅ Добавляем ID бота в ACL
    me = await bot.get_me()
    if not isinstance(settings.acl_ids, set):
        settings.acl_ids = set(settings.acl_ids)  # на всякий случай, если было list/tuple
    settings.acl_ids.add(me.id)
    logging.info(f"Bot @{me.username} (id={me.id}) добавлен в ACL")

    # Роутеры
    dp.include_router(zabbix_handler_router)

    # Старт
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")

