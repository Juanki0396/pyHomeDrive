import sqlite3

import click
from flask import Flask, current_app
from flask.cli import with_appcontext


class Database:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path

    def __enter__(self):
        self.db = sqlite3.connect(
            self.database_path, detect_types=sqlite3.PARSE_DECLTYPES
        )

        self.db.row_factory = sqlite3.Row
        return self.db

    def __exit__(self, type, value, traceback):
        self.db.close()

        if type is not None:
            print(type)
            print(value)
            print(traceback)

        return True


def get_db() -> Database:
    return Database(current_app.config["DATABASE"])


def init_db():
    database = get_db()
    with current_app.open_resource("schema.sql") as file:
        sql_command = file.read().decode("utf8")

    with database as db:
        db.executescript(sql_command)


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app: Flask) -> None:
    app.cli.add_command(init_db_command)


if __name__ == "__main__":
    pass
