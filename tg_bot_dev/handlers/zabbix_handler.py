from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from tg_bot_dev.settings import settings
from tg_bot_dev.services import Parser
from tg_bot_dev.keyboards import main_menu, main_menu_admin
from tg_bot_dev.utils import get_main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Приветственное сообщение. Клавиатура только для ACL."""
    menu = get_main_menu(message)
    if menu:
         await message.answer(
            "Привет!\nЭтот бот создан, чтобы облегчить просмотр алертов. Он выводит сообщения об ошибках, возникших за последнее время и актуальных на момент обращения.\nИспользуй кнопки для управления ботом",
            reply_markup=menu
        )
        
    return


# --- Общая логика отправки ---
async def send_alerts(message: Message, days: int):
    menu = get_main_menu(message)
    if not menu:
        return
    z = Parser()
    msgs = z.get_recent_problems(settings.zbx_uri, settings.zbx_user, settings.zbx_passwd, days)

    if not msgs:
        await message.answer(f"Алертов за {days} дней нет ✅", reply_markup=menu)
        return

    await message.answer("Alerts:")
    for m in msgs:
        await message.answer(m)
    await message.answer("Готово. Возврат в главное меню ⬇️", reply_markup=menu)

# --- Команды ---
@router.message(F.text==("Alerts за 3 дня"))
async def cmd_alerts_3(message: Message):
    print("1")
    await send_alerts(message, 3)

@router.message(F.text==("Alerts за 7 дней"))
async def cmd_alerts_7(message: Message):
    await send_alerts(message, 7)

@router.message(F.text==("Alerts за 30 дней"))
async def cmd_alerts_30(message: Message):
    await send_alerts(message, 30)

@router.message(F.text==("Alerts за 90 дней"))
async def cmd_alerts_90(message: Message):
    await send_alerts(message, 90)

