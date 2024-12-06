from app import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from pytz import UTC
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(200))
    date_created: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    confirmation: Mapped[bool] = mapped_column(default=False)

    @property
    def password(self):
        raise AttributeError("Password is not accesible")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"id: {self.id} - Username: {self.username} - email {self.email}"
