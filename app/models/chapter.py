# app/models/chapter.py

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Chapter(db.Model):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int]
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))

    __table_args__ = (
        UniqueConstraint("number", name="UQ_number"),
        UniqueConstraint("name", name="UQ_name"),
    )

    def __repr__(self) -> str:
        return f"{self.id} -- {self.number} - {self.name}\n"
