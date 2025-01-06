from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.routers.main.menu_router import menu_handler
from src.domain.interfaces.student_repository_interface import IStudentRepository


def setup_start_routes(router: Router, student_repository: IStudentRepository) -> None:
    @router.message(Command("start"))
    async def start_handler(message: Message, state: FSMContext):
        telegram_id = str(message.from_user.id)
        user = await student_repository.get_by_telegram_id(telegram_id)

        if user is None:
            greeting_text = (
                "Привет! Я бот, который поможет автоматически выбирать предметы в Old My SDU "
                "и обеспечит лёгкий доступ к платформе.\n\n"
                "Выбери один из вариантов:"
            )
            inline_kb = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Авторизоваться", callback_data="auth")
                    ],
                    [
                        InlineKeyboardButton(text="О приложении", callback_data="about")
                    ]
                ]
            )
            await message.answer(text=greeting_text, reply_markup=inline_kb)
            await state.clear()
        else:
            await menu_handler(message, state, student_repository)
