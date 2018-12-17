import logging
import os

import tornado.ioloop
from tornado.web import Application

from imdb.persistence import DBManager
from imdb.views.stats import (DesciptionHandler, FindHandler,
                              FindAllHandler, StatsHandler)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    dburl = os.environ.get('DBURL', 'mongodb://localhost:27017/')
    stats_port = os.environ.get('STATS_PORT', 8888)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    db = DBManager.getConnection(dburl)

    logger.info('Configurando ponto de acesso.')
    app = Application([
        ('/', DesciptionHandler, {'db': db}),
        ('/find', FindHandler, {'db': db}),
        ('/findall', FindAllHandler, {'db': db}),
        ('/stats', StatsHandler, {'db': db}),
    ])

    app.listen(stats_port)
    logger.info('Utilizando o banco {}.'.format(dburl))
    logger.info('Servidor configurado na porta {}.'.format(stats_port))
    logger.info('CTR+C para encerrar a aplicação')
    tornado.ioloop.IOLoop.current().start()
