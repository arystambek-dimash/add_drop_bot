from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.menu_handler import menu_handler
from src.domain.interfaces.student_repository_interface import IStudentRepository


def setup_menu_routes(student_repository: IStudentRepository) -> Router:
    router = Router()

    @router.message(Command("menu"))
    async def menu_command(message: Message, state: FSMContext):
        await menu_handler(message, state, student_repository)

    return router
