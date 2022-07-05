import os
import json

import flask


def create_app() -> flask.Flask:
    app = flask.Flask(__name__, instance_relative_config=True)

    app.config.from_file(
        os.path.join(app.instance_path, "application.json"), load=json.load
    )

    from . import views, auth, db

    db.init_app(app)  # Register database methods on the app
    app.register_blueprint(views.views, url_prefix="/")
    app.register_blueprint(auth.auth, url_prefix="/auth/")

    return app
