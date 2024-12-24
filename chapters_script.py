# chapters_script.py

import json

from app import create_app, db
from app.models import Chapter


def insert_chapters():
    """Inserts the chapters included in the chapters.json file into the db"""
    with open("chapters.json", encoding="utf-8") as chapter_file:
        data = json.load(chapter_file)

    chapters = [Chapter(**item) for item in data]

    app = create_app()

    with app.app_context():

        db.session.add_all(chapters)

        try:
            db.session.commit()
        except Exception as err:
            print("There was an error. The chapters weren't inserted into the db")
            print(err)
        else:
            print("Chapters inserted successully")


if __name__ == "__main__":
    insert_chapters()
