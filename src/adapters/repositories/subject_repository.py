from dataclasses import asdict
from typing import Optional, List
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.models.subject_orm import SubjectModel
from src.domain.dto.subject_dto import SubjectDTO, SubjectResponseDTO


class SubjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._model = SubjectModel

    async def create(self, subject_dto: SubjectDTO) -> SubjectResponseDTO:
        stmt = (
            insert(self._model)
            .values(**asdict(subject_dto))
            .returning(self._model)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        return SubjectResponseDTO.from_model(result.scalar_one())

    async def get_by_id(self, subject_id: int) -> Optional[SubjectResponseDTO]:
        stmt = select(self._model).where(self._model.id == subject_id)
        result = await self._session.execute(stmt)
        subject = result.scalar_one_or_none()
        return SubjectResponseDTO.from_model(subject) if subject else None

    async def get_all(self, offset: int = 0, limit: int = 100) -> List[SubjectResponseDTO]:
        stmt = select(self._model).offset(offset).limit(limit)
        result = await self._session.execute(stmt)
        subjects = result.scalars().all()
        return [SubjectResponseDTO.from_model(subject) for subject in subjects]

    async def update(self, subject_id: int, subject_dto: SubjectDTO) -> Optional[SubjectResponseDTO]:
        stmt = (
            update(self._model)
            .where(self._model.id == subject_id)
            .values(**asdict(subject_dto))
            .returning(self._model)
        )
        result = await self._session.execute(stmt)
        subject = result.scalar_one_or_none()
        if subject:
            await self._session.commit()
            return SubjectResponseDTO.from_model(subject)
        return None

    async def delete(self, subject_id: int) -> bool:
        stmt = (
            delete(self._model)
            .where(self._model.id == subject_id)
            .returning(self._model.id)
        )
        result = await self._session.execute(stmt)
        deleted = result.scalar_one_or_none()
        if deleted:
            await self._session.commit()
            return True
        return False

    async def exists(self, subject_id: int) -> bool:
        stmt = select(self._model.id).where(self._model.id == subject_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def find_by_code(self, subject_code: str) -> Optional[SubjectResponseDTO]:
        stmt = select(self._model).where(self._model.subject_code == subject_code)
        result = await self._session.execute(stmt)
        subject = result.scalar_one_or_none()
        return SubjectResponseDTO.from_model(subject) if subject else None
