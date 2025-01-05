from typing import Optional, List, Protocol
from src.domain.dto.subject_dto import SubjectDTO, SubjectResponseDTO


class ISubjectRepository(Protocol):
    async def create(self, subject: SubjectDTO) -> SubjectResponseDTO:
        pass

    async def get_by_id(self, subject_id: int) -> SubjectResponseDTO:
        pass

    async def get_all(self) -> List[SubjectResponseDTO]:
        pass

    async def update(self, subject_id: int, student_dto: SubjectDTO) -> Optional[SubjectResponseDTO]:
        pass

    async def delete(self, subject_id: int) -> bool:
        pass

    async def exists(self, subject_id: int) -> bool:
        pass

    async def find_by_code(self, subject_code: str) -> Optional[SubjectResponseDTO]:
        pass
