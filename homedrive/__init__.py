import os
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "homedrive.sqlite")
    )

    # Check if instance path exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    @app.route("/home")
    def home_page():
        return "<h1>Home Page</h1>"

    from . import db

    db.init_app(app)  # Register database methods on the app

    return app
