import json

import flask
import flask_sslify
from flask.ext.cors import CORS

from . import edx_edge


app = flask.Flask(__name__)
app.debug = True

cors = CORS(app)
flask_sslify.SSLify(app, permanent=True)


@app.route("/", methods=["POST"])
def data():
    kwargs = flask.request.get_json()
    posts = list(edx_edge.get_all_posts(**kwargs))
    return json.dumps(posts)
