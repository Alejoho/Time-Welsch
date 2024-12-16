from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app import chapters, db
from .complements import check_chapter
from sqlalchemy import select
from app.models import CompletedChapter
from datetime import datetime
import pytz


bp = Blueprint("main_routes", __name__)


@bp.before_request
@login_required
def check_confirmed():
    if current_user.confirmation is False:
        flash("Por favor confirma tu cuenta!", "warning")
        return redirect(url_for("register_routes.unconfirmed"))


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


@bp.get("/capitulo/<int:number>")
@check_chapter
def show_chapter(number):
    # TODO: Change the logic to check if the current chapter is created
    if number > 3:
        return render_template("chapters/chapter_in_process.html", number=number)
    return render_template(f"chapters/chapter_{number}.html", number=number)


# TODO: Design the way to mark a chapter as completed


# LATER: Change the number variable by chapter_number across the board
@bp.get("/capitulo/<int:number>/completado")
@check_chapter
def mark_chapter_as_completed(number):
    # update the current_chapters row of the current user
    current_user.current_chapter.current_chapter = number + 1
    # add a new row to the completed_chapters table for the current chapter an user
    completed_chapter = CompletedChapter(
        user_id=current_user.id,
        chapter_id=number,
        completed_date=datetime.now(pytz.utc),
    )

    db.session.add(completed_chapter)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        abort(500)
    # redirect the user to the next chapter
    return redirect(url_for("main_routes.show_chapter", number=number + 1))
