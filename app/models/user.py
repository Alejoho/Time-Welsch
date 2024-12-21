from datetime import datetime

import pytz
from flask_login import UserMixin
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(200))
    date_created: Mapped[datetime] = mapped_column(default=datetime.now(pytz.utc))
    confirmation: Mapped[bool] = mapped_column(default=False)
    # TODO: Add a new column to the db to mark a user as a demo_user in order to delete it when the session is close or other condition is meet
    current_chapter_relationship: Mapped["CurrentChapter"] = relationship(
        cascade="save-update, merge, delete"
    )

    __table_args__ = (
        UniqueConstraint("username", name="UQ_username"),
        UniqueConstraint("email", name="UQ_email"),
    )

    @property
    def password(self):
        raise AttributeError("Password is not accesible")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def current_chapter(self):
        return self.current_chapter_relationship.current_chapter

    @current_chapter.setter
    def current_chapter(self, value):
        self.current_chapter_relationship.current_chapter = value

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"id: {self.id} - Username: {self.username} - email {self.email}"
