from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.main_menu_handler import menu_handler
from src.domain.interfaces.student_repository_interface import IStudentRepository


def setup_menu_routes(router: Router, student_repository: IStudentRepository) -> None:
    @router.message(Command("menu"))
    async def menu_command(message: Message, state: FSMContext):
        await menu_handler(message, state, student_repository)
