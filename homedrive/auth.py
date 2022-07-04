import functools

from flask import current_app, Blueprint, render_template, request, session, url_for

from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login")
def login_page():
    return render_template("login.html")


@bp.route("/register")
def register_page():
    return render_template("register.html")
