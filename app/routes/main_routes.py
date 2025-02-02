# app/routes/main_routes.py

from datetime import datetime

import pytz
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from app import chapters, db
from app.models import CompletedChapter

from .complements import chapter_dont_exist
from .decorators import block_unconfirmed_users, check_chapter

bp = Blueprint("main_routes", __name__)


@bp.before_request
@login_required
@block_unconfirmed_users
# This is just a function to avoid and error
def bypass_error():
    pass


@bp.context_processor
def inject_chapters():
    return dict(chapters=chapters)


@bp.get("/mi-ruta")
def my_route():
    return render_template("main/my_route.html")


@bp.get("/resumen")
def summary():
    completed_chapters = db.session.scalars(
        select(CompletedChapter)
        .where(CompletedChapter.user_id == current_user.id)
        .order_by(CompletedChapter.completed_date)
    ).all()

    return render_template("main/summary.html", completed_chapters=completed_chapters)


@bp.get("/capitulo/<int:chapter_number>")
@check_chapter
def show_chapter(chapter_number):

    if chapter_dont_exist(chapter_number):
        return render_template("chapters/chapter_in_process.html")

    return render_template(
        f"chapters/chapter_{chapter_number}.html", chapter_number=chapter_number
    )


@bp.get("/capitulo/<int:chapter_number>/completado")
@check_chapter
def mark_chapter_as_completed(chapter_number):
    # update the current_chapters row of the current user
    current_user.current_chapter = chapter_number + 1
    # add a new row to the completed_chapters table for the current chapter an user
    completed_chapter = CompletedChapter(
        user_id=current_user.id,
        chapter_id=chapter_number,
        completed_date=datetime.now(pytz.utc),
    )

    db.session.add(completed_chapter)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)

    # redirect the user to the completed course page after completion of the app
    if chapter_number == (len(chapters) - 1):
        return render_template("main/completed_course.html")

    # redirect the user to the next chapter
    return redirect(
        url_for("main_routes.show_chapter", chapter_number=chapter_number + 1)
    )
