from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from website import app

http_server = HTTPServer(WSGIContainer(app))
print "Serving on port 80"
http_server.listen(80)
IOLoop.instance().start()
