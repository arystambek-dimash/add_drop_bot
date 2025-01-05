from aiogram import Dispatcher

from src.bot.routers.main.auth_router import setup_auth_routes
from src.bot.routers.common_router import router as common_router
from src.bot.routers.main.menu_router import setup_menu_routes
from src.bot.routers.main.start_routes import setup_start_routes
from src.bot.routers.student.menu import student_menu_router
from src.bot.routers.student.profile import setup_profile_routes
from src.domain.interfaces.student_repository_interface import IStudentRepository


def register_routers(dp: Dispatcher, student_repository: IStudentRepository):
    dp.include_router(setup_auth_routes(student_repository))
    dp.include_router(setup_start_routes(student_repository))
    dp.include_router(setup_menu_routes(student_repository))
    dp.include_router(common_router)
    dp.include_router(student_menu_router)
    dp.include_router(setup_profile_routes(student_repository))
