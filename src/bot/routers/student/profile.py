import json

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.adapters.parser.profile_page_service import parse_profile_page
from src.domain.interfaces.student_repository_interface import IStudentRepository


def setup_profile_routes(student_repository: IStudentRepository):
    router = Router()

    @router.callback_query(lambda c: c.data == "profile")
    async def profile_handler(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        user_id = data.get('user_id')
        print(user_id)
        user = await student_repository.get_by_telegram_id(user_id)
        profile_data = await parse_profile_page(json.loads(user.session_data))
        await callback.message.answer(profile_data)
        await callback.answer()

    return router
