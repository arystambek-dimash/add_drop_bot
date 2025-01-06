import json

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from src.adapters.parser.grades_page_service import parse_grades_page_service
from src.domain.interfaces.redis_repository_interface import IRedisRepository
from src.domain.interfaces.student_repository_interface import IStudentRepository
from src.domain.exceptions import ValidationError


def setup_grades_routes(
        router: Router,
        student_repository: IStudentRepository,
        redis_repository: IRedisRepository
) -> None:
    @router.callback_query(lambda c: c.data == "grades")
    async def grades_main_handler(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        user = await student_repository.get_by_telegram_id(str(user_id))
        session_data = await redis_repository.get(user.telegram_id)
        if not session_data:
            await callback.answer("Нет сессии. Пожалуйста, авторизуйтесь.")
            return
        terms = await redis_repository.get()
        try:
            parsed_data = await parse_grades_page_service(
                cookies_dict=json.loads(session_data),
            )
            print(parsed_data)
        except Exception as e:
            await  callback.answer(f"Ошибка при получении списка оценок: {str(e)}")
            return
        await redis_repository.set(
            f"grades_data:{user.telegram_id}",
            json.dumps(parsed_data),
            expire=604800  # 7 days
        )

        # each table => a term
        all_terms = parsed_data.get("grades", [])
        if not all_terms:
            await callback.answer("Оценки не найдены.")
            return

        # Build the inline keyboard
        kb_rows = []
        for i, term_block in enumerate(all_terms):
            term_label = term_block.get("term_label", f"Term #{i}")
            callback_data = f"grades_select:{i}"
            btn = InlineKeyboardButton(text=term_label, callback_data=callback_data)
            kb_rows.append([btn])

        # A "back" button to main menu
        back_btn = InlineKeyboardButton(text="← Вернуться к меню", callback_data="old_my_sdu_menu")
        kb_rows.append([back_btn])

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb_rows)

        await callback.message.edit_text(
            text="Выберите семестр, чтобы посмотреть оценки:",
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data and c.data.startswith("grades_select:"))
    async def view_grades_handler(callback: CallbackQuery, state: FSMContext):
        """
        Shows the courses for a selected term index
        """
        user_id = callback.from_user.id
        user = await student_repository.get_by_telegram_id(str(user_id))

        try:
            # parse the index from callback_data like "grades_select:0"
            _, str_index = callback.data.split(":")
            term_index = int(str_index)
        except ValueError:
            raise ValidationError("Неверный формат данных для выбора семестра!")

        # load from Redis
        stored = await redis_repository.get(f"grades_data:{user.telegram_id}")
        if not stored:
            raise ValidationError("Данные об оценках не найдены в кеше.")

        parsed_data = json.loads(stored)
        all_terms = parsed_data.get("grades", [])
        if term_index < 0 or term_index >= len(all_terms):
            raise ValidationError("Индекс семестра вне диапазона.")

        term_block = all_terms[term_index]
        term_label = term_block.get("term_label", f"Term #{term_index}")
        courses = term_block.get("courses", [])

        # Build message
        lines = [f"<b>{term_label}</b>"]
        if not courses:
            lines.append("Нет курсов в этом семестре.")
        else:
            for course in courses:
                code = course.get("course_code", "")
                name = course.get("course_name", "")
                total = course.get("total_grade", "")
                letter = course.get("letter_grade", "")
                lines.append(f"• <b>{code}</b> {name} — {letter} ({total})")

        text_msg = "\n".join(lines)

        # Back to terms
        back_button = InlineKeyboardButton(
            text="← Вернуться к семестрам",
            callback_data="grades"  # reuse the original "grades" callback
        )
        back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])

        await callback.message.edit_text(
            text_msg,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard
        )
        await callback.answer()
