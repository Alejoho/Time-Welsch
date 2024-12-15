from app import db
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint, Index
from datetime import datetime


class CompletedChapter(db.Model):
    __tablename__ = "completed_chapters"
    user_id: Mapped[int]
    chapter_id: Mapped[int]
    completed_date: Mapped[datetime]

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "chapter_id", name="PK_completed_chapters"),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="FK_completed_chapters_user_id"
        ),
        ForeignKeyConstraint(
            ["chapter_id"],
            ["chapters.id"],
            name="FK_completed_chapters_chapter_id",
        ),
        Index("idx_completed_chapters_user_id", "user_id"),
    )

    def __repr__(self):
        return f"user_id: {self.user_id} - current_id: {self.chapter_id} - {self.date}"
