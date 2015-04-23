
import flask
import flask_sslify
from . import edx_edge


app = flask.Flask(__name__)
app.debug = True

flask_sslify.SSLify(app, permanent=True)


@app.route("/", methods=["POST"])
def data():
    kwargs = flask.request.form.to_dict(flat=True)
    return ', '.join(edx_edge.get_all_posts(**kwargs))
