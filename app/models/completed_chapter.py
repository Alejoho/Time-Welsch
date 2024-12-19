from app import db
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint, Index
from datetime import datetime
import pytz


# LATER: Clean up all the models like this one. first all the things related with the
# table creation and the the things related with the logic of the app
class CompletedChapter(db.Model):
    __tablename__ = "completed_chapters"
    user_id: Mapped[int]
    chapter_id: Mapped[int]
    completed_date: Mapped[datetime]

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "chapter_id", name="PK_completed_chapters"),
        ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="FK_completed_chapters_user_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["chapter_id"],
            ["chapters.id"],
            name="FK_completed_chapters_chapter_id",
        ),
        Index("idx_completed_chapters_user_id", "user_id"),
    )

    @property
    def iso_completed_date(self):
        utc_datetime = self.completed_date.replace(tzinfo=pytz.utc)
        iso_format = utc_datetime.isoformat()
        return iso_format

    def __repr__(self):
        return f"user_id: {self.user_id} - current_id: {self.chapter_id} - {self.completed_date}"
