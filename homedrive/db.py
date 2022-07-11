import sqlite3
import typing

import click
import flask
import flask.cli


def get_db() -> sqlite3.Connection:
    """Create a database connection for the current app context and store it in
    the request.g object

    Returns:
        sqlite3.Connection: Database connection
    """
    db = getattr(flask.g, "_database", None)
    if db is None:
        flask.g._database = sqlite3.connect(flask.current_app.config["DATABASE"])
        db = flask.g._database
    db.row_factory = sqlite3.Row
    return db


def close_connection(exception: Exception) -> None:
    """Close database connection stored in flask.g object related to the app context.

    Args:
        exception (Exception): Any kind of raised exception
    """
    db = getattr(flask.g, "_database", None)
    if db is not None:
        db.close()


def query_db(query: str, args: typing.Tuple[typing.Any]) -> typing.List[sqlite3.Row]:
    """Returns a query from the app database"""
    cur = get_db().execute(query, args)
    results = cur.fetchall()
    cur.close()
    return results


def init_db() -> None:
    """ "Initialize the database using the sql schema."""
    database = get_db()
    with flask.current_app.open_resource("schema.sql") as file:
        sql_command = file.read().decode("utf8")

    with database as db:
        db.executescript(sql_command)


@click.command("init-db")
@flask.cli.with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app: flask.Flask) -> None:
    """Register the init-db command in the current app."""
    app.cli.add_command(init_db_command)
    app.teardown_appcontext(close_connection)


if __name__ == "__main__":
    pass
