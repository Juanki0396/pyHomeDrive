import flask

views = flask.Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return flask.render_template("home.html")
