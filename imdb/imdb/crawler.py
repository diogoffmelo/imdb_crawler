import json

import tornado.ioloop
from tornado.web import RequestHandler, Application

from imdb.persistence import DBManager
from imdb.numeric import StatVector


import logging
from pprint import pformat
import threading

from imdb.engine import RequestsEngine
from imdb.spider import IMDBSpider
from imdb.persistence import MongoDB

logger = logging.getLogger(__name__)

def log_item(item):
    item_str = pformat(
        {k: v for k, v in item.items() if k[0] != '_'})
    logger.info('Novo item:')
    logger.info(item_str)
    return item


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    db = DBManager.getConnection('mongodb://localhost:27017/')
    engine = RequestsEngine(IMDBSpider)
    engine.add_item_hook(log_item)
    engine.add_item_hook(db.persist)

    class EngineWrapper(object):
        def __init__(self):
            self.t = threading.Thread(target=engine.run)
        
        def run_engine(self):
            if not self.t.is_alive():
                self.t = threading.Thread(target=engine.run, kwargs={'pagination': 1})
                self.t.start()

    wrapper = EngineWrapper()
    class StartHandler(RequestHandler):
        def get(self):
            wrapper.run_engine()
            self.write(engine.get_status())

    class StatusHandler(RequestHandler):
        def get(self):
            self.write(engine.get_status())

    app = Application([
        ("/start", StartHandler),
        ("/status", StatusHandler),
    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
