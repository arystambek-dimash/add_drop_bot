import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.database.postgres import Base


class SubjectModel(Base):
    __tablename__ = 'wish_subjects'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('students.id'))
    subject_name: Mapped[str] = mapped_column(sa.String)
    subject_code: Mapped[str] = mapped_column(sa.String)
    teacher_name: Mapped[str] = mapped_column(sa.String, null=True)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
