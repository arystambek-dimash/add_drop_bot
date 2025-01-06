from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.handlers.start_menu_handler import start_menu_handler
from src.bot.routers.main.menu_router import menu_handler
from src.domain.interfaces.student_repository_interface import IStudentRepository


def setup_start_routes(router: Router, student_repository: IStudentRepository) -> None:
    @router.message(Command("start"))
    async def start_handler(message: Message, state: FSMContext):
        telegram_id = str(message.from_user.id)
        user = await student_repository.get_by_telegram_id(telegram_id)

        if user is None:
            await start_menu_handler(message, True)
            await state.clear()
        else:
            await menu_handler(message, state, student_repository)
