# app/scheduled_jobs.py

from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app import db, scheduler
from app.models import User


def delete_demo_users():
    """Deletes the demo users with a day of created."""
    deadline = datetime.now(UTC) - timedelta(days=1)

    with scheduler.app.app_context():
        user_to_delete = db.session.scalars(
            select(User).where((User.is_demo == True) & (User.date_created < deadline))
        ).all()

        for user in user_to_delete:
            db.session.delete(user)

        db.session.commit()

    print("Task done. Demo users deleted successfully.")
