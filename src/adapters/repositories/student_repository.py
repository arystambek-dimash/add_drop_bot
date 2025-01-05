from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional, List

from src.adapters.models.student_orm import StudentModel
from src.domain.dto.student_dto import StudentDTO


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, student_dto: StudentDTO) -> StudentDTO:
        student_model = student_dto.to_model(StudentModel)
        self._session.add(student_model)
        await self._session.commit()
        await self._session.refresh(student_model)
        return StudentDTO.from_model(student_model)

    async def get_by_telegram_id(self, telegram_id: str) -> Optional[StudentDTO]:
        stmt = select(StudentModel).where(StudentModel.telegram_id == telegram_id)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return StudentDTO.from_model(model) if model else None

    async def get_all(self) -> List[StudentDTO]:
        stmt = select(StudentModel)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [StudentDTO.from_model(m) for m in models]

    async def update(self, student_dto: StudentDTO) -> Optional[StudentDTO]:
        values = asdict(student_dto)

        stmt = (
            update(StudentModel)
            .where(StudentModel.telegram_id == student_dto.telegram_id)
            .values(**values)
            .returning(StudentModel)
        )

        result = await self._session.execute(stmt)
        updated_model = result.scalars().first()

        if not updated_model:
            return None

        await self._session.commit()
        await self._session.refresh(updated_model)

        return StudentDTO.from_model(updated_model)

    async def delete(self, telegram_id: str) -> bool:
        existing = await self._session.get(StudentModel, telegram_id)
        if not existing:
            return False

        await self._session.delete(existing)
        await self._session.commit()
        return True

    async def update_session_data(self, telegram_id: str, session_data: str) -> bool:
        stmt = (
            update(StudentModel)
            .where(StudentModel.telegram_id == telegram_id)
            .values(session_data=session_data)
            .returning(StudentModel)
        )

        result = await self._session.execute(stmt)
        updated_model = result.scalars().first()

        if not updated_model:
            return False

        await self._session.commit()
        return True

    async def get_session_data(self, telegram_id: str) -> Optional[str]:
        stmt = select(StudentModel.session_data).where(StudentModel.telegram_id == telegram_id)
        result = await self._session.execute(stmt)
        session_data = result.scalars().first()
        return session_data
