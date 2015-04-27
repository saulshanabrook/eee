import os
import logging

from livereload import Server

from .server import app

app.debug = True
logging.basicConfig(level=logging.DEBUG)
