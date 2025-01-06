from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.handlers.common_keyboards import get_menu_keyboard
from src.bot.handlers.start_menu_handler import start_menu_handler
from src.domain.interfaces.redis_repository_interface import IRedisRepository
from src.domain.interfaces.student_repository_interface import IStudentRepository


def setup_common_router(router: Router,
                        student_repository: IStudentRepository,
                        redis_repository: IRedisRepository) -> None:
    @router.callback_query(lambda c: c.data == "logout")
    async def logout_handler(callback: CallbackQuery) -> None:
        user_id = callback.from_user.id
        print(user_id)
        student = await student_repository.get_by_telegram_id(str(user_id))
        student.is_active = False
        await student_repository.update(student)
        await redis_repository.delete(str(user_id))
        await start_menu_handler(callback.message, False)

    @router.callback_query(lambda c: c.data == "go_back_main_menu")
    async def go_back_main_menu(callback: CallbackQuery, state: FSMContext):
        inline_kb = get_menu_keyboard()
        await callback.message.edit_text(
            text="Главное меню",
            reply_markup=inline_kb
        )
        await callback.answer()
