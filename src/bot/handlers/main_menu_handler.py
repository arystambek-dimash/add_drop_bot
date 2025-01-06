from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.handlers.common_keyboards import get_menu_keyboard
from src.domain.interfaces.student_repository_interface import IStudentRepository


async def menu_handler(message: Message, state: FSMContext, student_repository: IStudentRepository):
    telegram_id = str(message.from_user.id)
    user = await student_repository.get_by_telegram_id(telegram_id)

    if not user:
        await message.answer("Вы не авторизованы! Нажмите /start для входа.")
        return

    first_name = user.first_name
    last_name = user.last_name
    menu_text = f"👋 {first_name} {last_name}"

    inline_kb = get_menu_keyboard()
    await message.answer(menu_text, reply_markup=inline_kb)
    await state.clear()
