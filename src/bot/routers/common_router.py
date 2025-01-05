from aiogram import Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Update, ErrorEvent, Message

from src.domain.exceptions import ValidationError, NotFound, AlreadyExists, InternalServerError

router = Router()


@router.error(ExceptionTypeFilter(ValidationError), F.update.message.as_("message"))
async def handle_validation_error(event: ErrorEvent, message: Message):
    await message.answer(str(event.exception))


@router.error(ExceptionTypeFilter(NotFound), F.update.message.as_("message"))
async def handle_not_found_error(event: ErrorEvent, message: Message):
    await message.answer(str(event.exception) or "Запрашиваемый ресурс не найден.")


@router.error(ExceptionTypeFilter(AlreadyExists), F.update.message.as_("message"))
async def handle_already_exists_error(event: ErrorEvent, message: Message):
    await message.answer(str(event.exception) or "Ресурс уже существует.")


@router.error(ExceptionTypeFilter(InternalServerError), F.update.message.as_("message"))
async def handle_internal_server_error(event: ErrorEvent, message: Message):
    await message.answer(str(event.exception) or "Произошла внутренняя ошибка сервера. Попробуйте позже.")


@router.errors()
async def handle_general_exception(update: Update, exception: Exception):
    if isinstance(exception, TelegramAPIError):
        message = "Ошибка Telegram API. Пожалуйста, попробуйте позже."
    else:
        message = "Неизвестная ошибка. Обратитесь в службу поддержки."
    print(f"Произошла ошибка: {exception}")
    if update.message:
        await update.message.answer(message)

    return True
