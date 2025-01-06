import json

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from src.adapters.parser.transcript_page_service import parse_transcript_service
from src.domain.interfaces.redis_repository_interface import IRedisRepository
from src.domain.interfaces.student_repository_interface import IStudentRepository


def human_readable_semester(raw_semester: str) -> str:
    try:
        left_part, number_part = raw_semester.rsplit('.', maxsplit=1)
        left_part = left_part.strip()
        sem_number = number_part.strip()

        if sem_number == "1":
            sem_text = "Осенний семестр"
        elif sem_number == "2":
            sem_text = "Весенний семестр"
        else:
            sem_text = f"Семестр {sem_number}"

        left_part = left_part.replace(" - ", "–")

        return f"{left_part} ({sem_text})"
    except:
        return raw_semester


def setup_transcript_routes(
        router: Router,
        student_repository: IStudentRepository,
        redis_repository: IRedisRepository
) -> None:
    @router.callback_query(lambda c: c.data == "transcript")
    async def transcript_handler(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id

        user = await student_repository.get_by_telegram_id(str(user_id))
        session_data = await redis_repository.get(user.telegram_id)
        if not session_data:
            await callback.answer("Сессия не найдена. Пожалуйста, войдите снова.")
            return

        try:
            transcript_data = await parse_transcript_service(json.loads(session_data))
        except Exception as e:
            await callback.answer(f"Ошибка при получении транскрипта: {str(e)}")
            return

        if not transcript_data:
            await callback.answer("Данные транскрипта не найдены.")
            return

        await redis_repository.set(
            f"transcript_data:{user.telegram_id}",
            json.dumps(transcript_data),
            expire=604800
        )

        keyboard_rows = []
        for index, semester_info in enumerate(transcript_data):
            raw_name = semester_info.get("semester_name", f"Семестр #{index + 1}")
            hr_name = human_readable_semester(raw_name)

            button = InlineKeyboardButton(
                text=hr_name,
                callback_data=f"view_semester:{index}"
            )
            keyboard_rows.append([button])
        back_button = InlineKeyboardButton(
            text="← Вернуться к меню",
            callback_data="old_my_sdu_menu"
        )
        keyboard_rows.append([back_button])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)

        await callback.message.edit_text(
            "Выберите семестр, чтобы посмотреть оценки:",
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
        await callback.answer()

    @router.callback_query(lambda c: c.data and c.data.startswith("view_semester:"))
    async def view_semester_handler(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        user = await student_repository.get_by_telegram_id(str(user_id))

        try:
            _, str_index = callback.data.split(":")
            semester_index = int(str_index)
        except ValueError:
            await callback.answer("Неверный индекс семестра!")
            return

        stored_data = await redis_repository.get(f"transcript_data:{user.telegram_id}")
        if not stored_data:
            await callback.answer("Данные транскрипта не найдены в кеше.")
            return

        transcript_data = json.loads(stored_data)

        if semester_index < 0 or semester_index >= len(transcript_data):
            await callback.answer("Индекс семестра вне диапазона.")
            return

        semester_info = transcript_data[semester_index]
        raw_semester_name = semester_info.get("semester_name", "Без названия")
        semester_name = human_readable_semester(raw_semester_name)

        lines = [f"<b>{semester_name}</b>"]
        courses = semester_info.get("courses", [])

        if not courses:
            lines.append("В этом семестре курсов не найдено.")
        else:
            for course in courses:
                code = course.get("course_code", "")
                title = course.get("course_title", "")
                numeric = course.get("numeric_grade", "")
                letter = course.get("letter_grade", "")
                lines.append(f"• <b>{code}</b> {title} — {letter} ({numeric})")

        footer = semester_info.get("footer", {})
        if footer:
            lines.append("")
            lines.append("<b>Статистика семестра</b>")
            lines.append(f"• Кредиты: {footer.get('credits_semester', '')}")
            lines.append(f"• ECTS: {footer.get('ects_semester', '')}")
            lines.append(f"• Средний балл (SA): {footer.get('SA', '')}")
            lines.append(f"• Средний процент (GA): {footer.get('GA', '')}")
            lines.append(f"• Семестровый GPA (SPA): {footer.get('SPA', '')}")
            lines.append(f"• Итоговый GPA: {footer.get('GPA', '')}")

        reply_text = "\n".join(lines)

        back_button = InlineKeyboardButton(
            text="← Вернуться к семестрам",
            callback_data="transcript"
        )
        back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])

        await callback.message.edit_text(
            reply_text,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard
        )
        await callback.answer()