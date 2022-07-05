import functools
import sqlite3

import flask
from werkzeug import security

from .db import get_db

auth = flask.Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login")
def login():
    return flask.render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        email = flask.request.form["email"]
        password = flask.request.form["password"]

    return flask.render_template("register.html")
