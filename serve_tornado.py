from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from website import app

http_server = HTTPServer(WSGIContainer(app))
print "Serving on port 5000"
http_server.listen(5000)
IOLoop.instance().start()
