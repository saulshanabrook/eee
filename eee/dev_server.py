import os

from livereload import Server
import werkzeug.debug

from . import server

app = werkzeug.debug.DebuggedApplication(server.app, evalex=True)

server = Server(app)
server.watch('eee/*.py')
server.serve(port=os.environ['PORT'])
