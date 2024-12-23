# run.py

from app import create_app

app = create_app()


@app.shell_context_processor
def make_shell_context():
    import sqlalchemy as sa
    import sqlalchemy.orm as so

    from app import db
    from app.models import User

    return {"sa": sa, "so": so, "db": db, "User": User}


if __name__ == "__main__":
    app.run(
        debug=app.config["DEBUG"], host="0.0.0.0", use_reloader=app.config["RELOAD"]
    )
