from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Chapter(db.Model):
    __tablename__ = "chapters"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500))
