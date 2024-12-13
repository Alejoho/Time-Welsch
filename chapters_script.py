from app import db, create_app
import json
from app.models import Chapter

with open("chapters.json", encoding="utf-8") as chapter_file:
    data = json.load(chapter_file)

chapters = [Chapter(**item) for item in data]

app = create_app()

with app.app_context():

    db.session.add_all(chapters)

    try:
        db.session.commit()
    except:
        print("There was an error. The chapters weren't added to the db")
    else:
        print("Chapters imported successully")
