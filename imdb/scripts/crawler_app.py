import logging
import os
from pprint import pformat
import threading

import tornado.ioloop
from tornado.web import Application

from imdb.engine import RequestsEngine
from imdb.persistence import DBManager
from imdb.views.crawler import (DesciptionHandler, StartHandler,
                                StatusHandler)


from imdb.spider import IMDBSpider
from imdb.persistence import DBManager

logger = logging.getLogger(__name__)


def log_item(item):
    item_str = pformat(
        {k: v for k, v in item.items() if k[0] != '_'})
    logger.info('Novo item:')
    logger.info(item_str)
    return item


if __name__ == '__main__':
    dburl = os.environ.get('DBURL', 'mongodb://localhost:27017/')
    crawler_port = os.environ.get('CRAWLER_PORT', 8889)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    logger.info('Configurando ponto de acesso.')

    db = DBManager.getConnection(dburl)
    engine = RequestsEngine(IMDBSpider)
    engine.add_item_hook(log_item)
    engine.add_item_hook(db.persist)

    class EngineWrapper(object):
        def __init__(self):
            self.t = None
        
        def run(self, paginacao=1):
            if not self.t or not self.t.is_alive():
                self.t = threading.Thread(
                    target=engine.run, kwargs={'paginacao': paginacao})
                self.t.start()

        def get_status(self):
            return engine.get_status()

    wrapper = EngineWrapper()

    app = Application([
        ('/', DesciptionHandler),
        ('/start', StartHandler, {'engine': wrapper}),
        ('/status', StatusHandler, {'engine': wrapper}),
    ])

    app.listen(crawler_port)
    logger.info('Utilizando o banco {}.'.format(dburl))
    logger.info('Servidor configurado na porta {}.'.format(crawler_port))
    logger.info('CTR+C para encerrar a aplicação')
    tornado.ioloop.IOLoop.current().start()

