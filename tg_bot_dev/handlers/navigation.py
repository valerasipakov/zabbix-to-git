from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot_dev.utils import get_main_menu, get_admin_zone_menu

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


@router.message(F.text==("Админ-зона"))
async def go_to_admin_zone(message: Message):
    menu = get_admin_zone_menu(message)
    if menu:
        await message.answer("Вы в админ зоне", reply_markup=menu)
    return

@router.message(F.text==("Основное меню"))
async def back_to_main_menu(message: Message):
    menu = get_main_menu(message)
    if menu:
        await message.answer("Вывод сообщений об ошибках", reply_markup=menu)
    return

