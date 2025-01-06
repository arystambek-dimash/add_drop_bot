import json

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from src.adapters.parser.year_terms_service import parse_year_terms_service
from src.adapters.parser.schedule_page_service import parse_schedule_page_service
from src.domain.interfaces.redis_repository_interface import IRedisRepository
from src.domain.interfaces.student_repository_interface import IStudentRepository


def setup_schedule_routes(
        router: Router,
        student_repository: IStudentRepository,
        redis_repository: IRedisRepository
) -> None:
    @router.callback_query(lambda c: c.data == "schedule")
    async def schedule_main_handler(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        user = await student_repository.get_by_telegram_id(str(user_id))
        session_data = await redis_repository.get(user.telegram_id)
        if not session_data:
            await callback.answer("Сессия не найдена. Пожалуйста, войдите снова.")
            return

        cookies = json.loads(session_data)
        try:
            year_term_list = await parse_year_terms_service(cookies)
        except Exception as e:
            await callback.answer(f"Ошибка при поиске год/семестр: {str(e)}")
            return

        kb_rows = []
        for yt in year_term_list:
            year = yt["year"]
            term = yt["term"]
            label = yt["label"]

            cb_data = f"schedule_select:{year}:{term}"
            btn = InlineKeyboardButton(text=label, callback_data=cb_data)
            kb_rows.append([btn])
        back_btn = InlineKeyboardButton(text="← Вернутся к меню", callback_data="old_my_sdu_menu")
        kb_rows.append([back_btn])
        dynamic_kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)

        await callback.message.edit_text(
            text="Выберите год и семестр:",
            reply_markup=dynamic_kb,
            parse_mode=ParseMode.HTML
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data and c.data.startswith("schedule_select:"))
    async def schedule_show_handler(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        user = await student_repository.get_by_telegram_id(str(user_id))
        session_data = await redis_repository.get(user.telegram_id)
        if not session_data:
            await callback.answer("Сессия не найдена. Пожалуйста, войдите снова.")
            return

        try:
            _, str_year, str_term = callback.data.split(":")
            year = int(str_year)
            term = int(str_term)
        except ValueError:
            await callback.answer("Неправильный формат year/term!")
            return

        cookies = json.loads(session_data)

        try:
            schedule_dict = await parse_schedule_page_service(
                cookies_dict=cookies,
                year=year,
                term=term
            )
        except Exception as e:
            await callback.answer(f"Ошибка при получении расписания: {str(e)}")
            return

        year_term_display = schedule_dict.get("year_term", f"{year} (term {term})")
        schedule_rows = schedule_dict.get("schedule", [])

        lines = [f"<b>Расписание на {year_term_display}</b>\n"]

        for slot in schedule_rows:
            time_range = slot["time_range"]
            days_map = slot["days"]
            lines.append(f"<b>{time_range}</b>")
            for day_name, courses in days_map.items():
                if not courses:
                    continue
                course_codes = ", ".join(c["course_code"] for c in courses)
                lines.append(f"  {day_name}: {course_codes}")
            lines.append("")

        result_text = "\n".join(lines)

        if len(result_text) > 4000:
            result_text = result_text[:4000] + "\n... (расписание обрезано) ..."

        back_button = InlineKeyboardButton(
            text="← Вернуться к семестрам",
            callback_data="schedule"
        )

        back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
        await callback.message.edit_text(result_text, parse_mode=ParseMode.HTML, reply_markup=back_keyboard)
        await callback.answer()
