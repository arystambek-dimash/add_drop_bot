import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.database.postgres import Base


class StudentModel(Base):
    __tablename__ = 'students'

    telegram_id: Mapped[str] = mapped_column(sa.String, primary_key=True, nullable=False)
    student_id: Mapped[str] = mapped_column(sa.String, nullable=True)
    student_password: Mapped[str] = mapped_column(sa.String, nullable=True)
    first_name: Mapped[str] = mapped_column(sa.String, nullable=True)
    last_name: Mapped[str] = mapped_column(sa.String, nullable=True)
    language: Mapped[str] = mapped_column(sa.String, default='ru')
    session_data: Mapped[str] = mapped_column(sa.Text, nullable=True)
