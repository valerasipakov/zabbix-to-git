import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Set

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(name)s: %(message)s",
)

@dataclass(frozen=True)
class Settings:
    token: str
    acl_ids: Set[int]

def get_settings() -> Settings:
    token = os.environ.get("BOT_TOKEN", "")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    raw_acl = os.environ.get("ACL_IDS", "").strip()
    acl_ids: Set[int] = set()
    if raw_acl:
        for part in raw_acl.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                acl_ids.add(int(part))
            except ValueError:
                logging.warning("Skip invalid ACL id: %r", part)

    if not acl_ids:
        logging.warning("ACL_IDS is empty — никто не сможет писать боту")
    return Settings(token=token, acl_ids=acl_ids)

settings = get_settings()
bot = Bot(token=settings.token)
dp = Dispatcher()

# --- Хелпер: проверка ACL ---
def is_allowed(msg: Message) -> bool:
    print(msg.from_user.id, settings.acl_ids, f'This {msg.from_user.id in settings.acl_ids}')
    uid = msg.from_user.id if msg.from_user else None
    return uid in settings.acl_ids

# --- Команды ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    if not is_allowed(message):
        await message.answer("⛔ Доступ запрещён.")
        return
    await message.answer(
        "Привет! Я эхо-бот. Отправь любое сообщение — я его продублирую.\n"
        "Команда /whoami покажет твой user_id."
    )

@dp.message(Command("whoami"))
async def cmd_whoami(message: Message):
    uid = message.from_user.id if message.from_user else None
    await message.answer(f"Ваш user_id: {uid}")

# --- Эхо-дублирование ---
@dp.message()  # ловим любые апдейты-сообщения
async def echo(message: Message):
    if not is_allowed(message):
        # Не палимся лишней болтовнёй — просто игнор
        return

    # Самый универсальный способ — копировать сообщение как есть
    try:
        await bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_to_message_id=message.message_id if message.reply_to_message else None
        )
    except Exception as e:
        logging.exception("Failed to copy message: %s", e)
        # fallback: хотя бы текстом
        if message.text:
            await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")

