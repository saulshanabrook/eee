
import flask
import flask_sslify
from flask.ext.cors import CORS

from . import edx_edge


app = flask.Flask(__name__)
app.debug = False

cors = CORS(app)
flask_sslify.SSLify(app, permanent=True)


@app.route("/", methods=["POST"])
def data():
    kwargs = flask.request.form.to_dict(flat=True)
    return ', '.join(edx_edge.get_all_posts(**kwargs))
