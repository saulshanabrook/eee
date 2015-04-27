import json

import flask
import flask_sslify
from flask.ext.cors import CORS

from .server import app


cors = CORS(app)
flask_sslify.SSLify(app, permanent=True)
