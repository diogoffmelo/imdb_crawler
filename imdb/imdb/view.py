import json

import tornado.ioloop
import tornado.web

from imdb.persistence import DBConn

db = DBConn()
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(db.fetchall()))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
