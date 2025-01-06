import dataclasses
from typing import Optional

from src.adapters.models.student_orm import StudentModel
from src.domain.interfaces.base_dto import BaseDTO


@dataclasses.dataclass
class StudentDTO(BaseDTO[StudentModel, "StudentDTO"]):
    telegram_id: str
    student_id: Optional[str] = None
    student_password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language: Optional[str] = None
    is_active: Optional[bool] = None
