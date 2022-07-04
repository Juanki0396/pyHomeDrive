import os
from flask import Flask, render_template


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
        return render_template("home.html")

    @app.route("/files")
    def files_page():
        return render_template("files.html")

    from . import db

    db.init_app(app)  # Register database methods on the app

    from . import auth

    app.register_blueprint(auth.bp)

    return app
