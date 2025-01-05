import dataclasses

from src.adapters.models.subject_orm import SubjectModel
from src.domain.interfaces.base_dto import BaseDTO


@dataclasses.dataclass
class SubjectDTO(BaseDTO[SubjectModel, "SubjectDTO"]):
    student_id: int
    subject_name: str
    subject_code: str
    teacher_name: str
    is_active: bool


@dataclasses.dataclass
class SubjectResponseDTO(BaseDTO[SubjectModel, "SubjectResponseDTO"]):
    id: int
    student_id: int
    subject_name: str
    subject_code: str
    teacher_name: str
    is_active: bool
