from aiogram import Dispatcher, Router

from src.bot.middleware import RedisSessionMiddleware
from src.bot.routers.main.auth_router import setup_auth_routes
from src.bot.routers.exception_router import router as common_router
from src.bot.routers.main.menu_router import setup_menu_routes
from src.bot.routers.main.start_routes import setup_start_routes
from src.bot.routers.student.grades_router import setup_grades_routes
from src.bot.routers.common_router import setup_common_router
from src.bot.routers.student.menu_router import student_menu_router
from src.bot.routers.student.profile_router import setup_profile_routes
from src.bot.routers.student.schedule_router import setup_schedule_routes
from src.bot.routers.student.transcript_router import setup_transcript_routes
from src.domain.interfaces.redis_repository_interface import IRedisRepository
from src.domain.interfaces.student_repository_interface import IStudentRepository


def register_routers(dp: Dispatcher, redis_repo: IRedisRepository, student_repository: IStudentRepository):
    router = Router()
    start_router = Router()
    """ start router """
    setup_start_routes(start_router, student_repository=student_repository)
    """ auth router """
    setup_auth_routes(start_router, student_repository=student_repository)
    """ menu router """
    setup_menu_routes(router, student_repository=student_repository)
    """ transcript router """
    setup_transcript_routes(router, student_repository=student_repository, redis_repository=redis_repo)
    """ profile router """
    setup_profile_routes(router, student_repository=student_repository, redis_repository=redis_repo)
    """ student router """
    setup_schedule_routes(router, student_repository=student_repository, redis_repository=redis_repo)
    """ grades router """
    setup_grades_routes(router, student_repository=student_repository, redis_repository=redis_repo)
    """ logout router """
    setup_common_router(start_router, student_repository=student_repository, redis_repository=redis_repo)

    """ initializing routers """
    dp.include_router(common_router)
    dp.include_router(student_menu_router)
    dp.include_router(router)
    dp.include_router(start_router)

    router.message.middleware(
        RedisSessionMiddleware(student_repository=student_repository, redis_repository=redis_repo))
    router.callback_query.middleware(
        RedisSessionMiddleware(student_repository=student_repository, redis_repository=redis_repo))
