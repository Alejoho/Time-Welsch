from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint


class Chapter(db.Model):
    __tablename__ = "chapters"

    # TODO: remove the column id and set the number as primary key but without autoincrementing
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
