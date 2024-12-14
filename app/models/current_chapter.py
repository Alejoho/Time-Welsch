from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
)
from app.models import User


class CurrentChapter(db.Model):
    __tablename__ = "current_chapters"
    id: Mapped[int]
    user_id: Mapped[int]
    # CHECK: This default only works through sqlalchemy. How can i make it work when inserting direct in the db
    current_chapter: Mapped[int] = mapped_column(default=1)

    __table_args__ = (
        # CHECK: How to give a name to the primarykey of the table not the default
        PrimaryKeyConstraint("id", name="PK_current_chapters"),
        UniqueConstraint("user_id", name="UQ_user_id"),
        ForeignKeyConstraint(["user_id"], ["users.id"], name="FK_user_id"),
    )

    def __repr__(self):
        return f"user_id: {self.user_id} - current_chapter: {self.current_chapter}"
