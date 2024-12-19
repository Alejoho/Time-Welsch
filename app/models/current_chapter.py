from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    UniqueConstraint,
    ForeignKeyConstraint,
)
from app.models import User


class CurrentChapter(db.Model):
    __tablename__ = "current_chapters"
    # LATER: Remove this id. And create a compound primary key with the other 2 columns
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    current_chapter: Mapped[int] = mapped_column(default=1)

    __table_args__ = (
        # LATER: Match the naming of the completed_chapters table. (UQ_current_chapters_user_id)
        UniqueConstraint("user_id", name="UQ_user_id"),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="FK_user_id", ondelete="CASCADE"
        ),
    )

    def __repr__(self):
        return f"user_id: {self.user_id} - current_chapter: {self.current_chapter}"
