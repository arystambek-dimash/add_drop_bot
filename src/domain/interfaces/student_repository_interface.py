from typing import Optional, List, Protocol
from src.domain.dto.student_dto import StudentDTO


class IStudentRepository(Protocol):
    async def create(self, student_dto: StudentDTO) -> StudentDTO:
        pass

    async def get_by_telegram_id(self, telegram_id: str) -> Optional[StudentDTO]:
        pass

    async def get_all(self) -> List[StudentDTO]:
        pass

    async def update(self, student_dto: StudentDTO) -> Optional[StudentDTO]:
        pass

    async def delete(self, telegram_id: str) -> bool:
        pass

    async def update_session_data(self, telegram_id: str, session_data: str) -> bool:
        pass

    async def get_session_data(self, telegram_id: str) -> Optional[str]:
        pass
