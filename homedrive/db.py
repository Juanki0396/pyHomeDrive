import sqlite3

import click
from flask import Flask, current_app
from flask.cli import with_appcontext


class DatabaseConnection:
    def __init__(self, database_path: str) -> None:
        """Instanciate a DatabaseConnection handler. It offers a Context Manager to create database connections
        safely.

        Args:
            database_path (str): Path of the database file
        """
        self.database_path = database_path
        self.db: sqlite3.Connection = None

    def __enter__(self) -> sqlite3.Cursor:
        """Start a database conection and return a cursor object."""
        self.db = sqlite3.connect(
            self.database_path, detect_types=sqlite3.PARSE_DECLTYPES
        )

        self.db.row_factory = sqlite3.Row

        return self.db.cursor()

    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:
        """Commit or close database connection if any error arise."""
        if exc_type is sqlite3.Error:
            print(exc_type)
            self.db.close()
            return False

        self.db.commit()
        self.db.close()

        return True


def get_db() -> DatabaseConnection:
    """Return a DatabaseConection object for the current Flask app."""
    return DatabaseConnection(current_app.config["DATABASE"])


def init_db() -> None:
    """ "Initialize the database using the sql schema."""
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
    """Register the init-db command in the current app."""
    app.cli.add_command(init_db_command)


if __name__ == "__main__":
    pass
