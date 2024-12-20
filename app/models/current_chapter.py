from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, PrimaryKeyConstraint


class CurrentChapter(db.Model):
    __tablename__ = "current_chapters"

    user_id: Mapped[int]
    current_chapter: Mapped[int] = mapped_column(default=1)

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "current_chapter", name="PK_current_chapters"),
        UniqueConstraint("user_id", name="UQ_user_id"),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="FK_user_id", ondelete="CASCADE"
        ),
    )

    def __repr__(self):
        return f"user_id: {self.user_id} - current_chapter: {self.current_chapter}"
