import json

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from src.adapters.parser.profile_page_service import parse_profile_page
from src.domain.interfaces.redis_repository_interface import IRedisRepository
from src.domain.interfaces.student_repository_interface import IStudentRepository


def setup_profile_routes(router: Router,
                         student_repository: IStudentRepository,
                         redis_repository: IRedisRepository) -> None:
    @router.callback_query(lambda c: c.data == "profile")
    async def profile_handler(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        user = await student_repository.get_by_telegram_id(str(user_id))
        session_data = await redis_repository.get(user.telegram_id)
        profile_data = await parse_profile_page(json.loads(session_data))
        back_button = InlineKeyboardButton(
            text="← Вернуться к меню",
            callback_data="old_my_sdu_menu"
        )
        back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])

        await callback.message.edit_text(profile_data, parse_mode=ParseMode.HTML, reply_markup=back_keyboard)
        await callback.answer()
