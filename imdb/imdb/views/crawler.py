import json

from tornado.web import RequestHandler

ERROR_JSON = {'status': 'InvalidArgument'}

DESCRIPTION_JSON = {
    '/status':
        'Estado da engine (crawler).',
    '/start?<paginacao=1>':
        '(Re)Inicializa a engina com a profundidade especificada.',
}


class DesciptionHandler(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(DESCRIPTION_JSON))


class StartHandler(RequestHandler):
    def initialize(self, engine):
        self.engine = engine

    def get(self):
        self.set_header('Content-Type', 'application/json')        
        
        paginacao = self.get_query_argument('paginacao', '1')

        try:
            paginacao = int(paginacao)
        except:
            self.write(json.dumps(ERROR_JSON))
            return

        self.engine.run(paginacao)
        self.write(self.engine.get_status())


class StatusHandler(RequestHandler):
    def initialize(self, engine):
        self.engine = engine

    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(self.engine.get_status())
