from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import json

from src.adapters.parser.home_page_service import parse_home_page_service
from src.adapters.parser.login_service import login_and_save_cookies
from src.adapters.utils.hash_pass import hash_password
from src.bot.handlers.menu_handler import menu_handler
from src.bot.states import StudentLoginState
from src.domain.dto.student_dto import StudentDTO
from src.domain.interfaces.student_repository_interface import IStudentRepository


def setup_auth_routes(student_repository: IStudentRepository) -> Router:
    router = Router()

    @router.callback_query(F.data == "auth")
    async def on_auth_button(callback: CallbackQuery, state: FSMContext):
        telegram_id = str(callback.message.from_user.id)
        user = await student_repository.get_by_telegram_id(telegram_id)

        if user is None:
            # Store the initial message ID
            await state.update_data(messages_to_delete=[callback.message.message_id])

            # Send and store username prompt message
            msg = await callback.message.answer("Пожалуйста, введите свой username в (Old My SDU):")
            state_data = await state.get_data()
            messages_to_delete = state_data.get('messages_to_delete', [])
            messages_to_delete.append(msg.message_id)
            await state.update_data(messages_to_delete=messages_to_delete)

            await state.set_state(StudentLoginState.WAITING_FOR_STUDENT_ID)
            await callback.answer()
            return

        await callback.answer("Вы уже авторизованный.")
        await menu_handler(callback.message, state, student_repository)

    @router.message(StudentLoginState.WAITING_FOR_STUDENT_ID)
    async def process_student_id(message: Message, state: FSMContext):
        # Store user's message ID
        state_data = await state.get_data()
        messages_to_delete = state_data.get('messages_to_delete', [])
        messages_to_delete.append(message.message_id)

        # Send and store password prompt message
        msg = await message.answer("Введите пароль:")
        messages_to_delete.append(msg.message_id)

        await state.update_data(
            username=message.text,
            messages_to_delete=messages_to_delete
        )
        await state.set_state(StudentLoginState.WAITING_FOR_PASSWORD)

    @router.message(StudentLoginState.WAITING_FOR_PASSWORD)
    async def process_password(message: Message, state: FSMContext):
        state_data = await state.get_data()
        messages_to_delete = state_data.get('messages_to_delete', [])
        messages_to_delete.append(message.message_id)
        await state.update_data(messages_to_delete=messages_to_delete)

        password = message.text
        user_data = await state.get_data()
        username = user_data.get("username")
        telegram_id = str(message.from_user.id)

        processing_msg = await message.answer("Обработка данных...")
        messages_to_delete.append(processing_msg.message_id)

        cookies = await login_and_save_cookies(username, password)
        full_name = await parse_home_page_service(cookies)

        if full_name:
            parts = full_name.split(maxsplit=1)
            first_name, last_name = parts if len(parts) == 2 else (full_name, "")

            await student_repository.create(
                StudentDTO(
                    telegram_id=telegram_id,
                    first_name=first_name,
                    last_name=last_name,
                    student_id=username,
                    student_password=hash_password(password),
                    session_data=json.dumps(cookies),
                )
            )

            for msg_id in messages_to_delete:
                try:
                    await message.bot.delete_message(message.chat.id, msg_id)
                except Exception:
                    pass
            success_msg = await message.answer("Авторизация успешна!")
            await menu_handler(message, state, student_repository)

            try:
                await message.bot.delete_message(message.chat.id, success_msg.message_id)
            except Exception:
                pass

        else:
            error_msg = await message.answer("Ошибка при парсинге имени пользователя.")
            messages_to_delete.append(error_msg.message_id)
            await state.update_data(messages_to_delete=messages_to_delete)

        await state.clear()

    return router
