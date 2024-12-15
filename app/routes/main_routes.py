from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import chapters, db
from .complements import check_chapter
from sqlalchemy import select
from app.models import CompletedChapter


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


@bp.get("/ejercicios")
def exercises():
    return render_template("main/exercises.html")


@bp.get("/capitulo/<int:number>")
@check_chapter
def show_chapter(number):
    if number > 3:
        return render_template("chapters/chapter_in_process.html", number=number)
    return render_template(f"chapters/chapter_{number}.html", number=number)


@bp.get("/test")
def test():
    # TODO: Evaluate the diffenrence between session.execute, session.scalars, session.execute().scalars. and also check the all
    return render_template("test.html")
