import os
import json

from flask import Flask, render_template

from . import db, auth


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_file(
        os.path.join(app.instance_path, "application.json"), load=json.load
    )

    @app.route("/")
    @app.route("/home")
    def home_page():
        return render_template("home.html")

    @app.route("/files")
    def files_page():
        return render_template("files.html")

    db.init_app(app)  # Register database methods on the app
    app.register_blueprint(auth.bp)

    return app
