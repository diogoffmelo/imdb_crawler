import json

import tornado.ioloop
from tornado.web import RequestHandler, Application

from imdb.persistence import MongoDB
from imdb.numeric import StatVector

ERROR_JSON = {'status': 'InvalidArgument'}

DESCRIPTION_JSON = {
    '/find?<skip=0>&<limit=50>':
    'Lista os filmes salvos banco de dados.',
    '/findall':
        'Lista todos os filmes salvos banco de dados (pode demorar).',
    '/stats':
        'Estatísticas dos filmes salvos.',
}


class AbstractHandler(RequestHandler):
    def initialize(self, db):
        self.db = db


class DesciptionHandler(AbstractHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(DESCRIPTION_JSON))


class FindHandler(AbstractHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        skip = self.get_query_argument('skip', '0')
        limit = self.get_query_argument('limit', '50')

        try:
            skip = int(skip)
            limit = int(limit)
        except:
            self.write(json.dumps(ERROR_JSON))
            return

        objs = list(db.find(skip=skip, limit=limit))
        for obj in objs:
            obj['_id'] = str(obj['_id'])

        self.write(json.dumps(objs))


class FindAllHandler(AbstractHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        objs = list(db.fetchall())
        for obj in objs:
            obj['_id'] = str(obj['_id'])

        self.write(json.dumps(objs))


class StatsHandler(AbstractHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        entities = StatVector(db.fetchall())

        genres = set()
        for genres_list in entities.map(lambda x: x['genero']):
            genres |= set(genres_list)

        rates = entities.\
            filter(lambda x: bool(x['rating'])).\
            map(lambda x: float(x['rating']))

        try:
            rate_stats = {
                'mean': rates.mean(),
                'std': rates.std(),
                'min': rates.min(),
                'max': rates.max(),
            }
        except Exception:
            rate_stats = {
                'mean': None,
                'std': None,
                'min': None,
                'max': None,
            }

        def duration_transform(entity):
            try:
                return float(entity['duracao'][0])
            except:
                pass

            return -1

        durations = entities.\
            map(duration_transform).\
            filter(lambda x: x > 0)

        try:
            duration_stats = {
                'mean': durations.mean(),
                'std': durations.std(),
                'min': durations.min(),
                'max': durations.max(),
            }
        except Exception:
            duration_stats = {
                'mean': None,
                'std': None,
                'min': None,
                'max': None,
            }

        genre_stats = {}
        for g in genres:
            rates_genre = entities.\
                filter(lambda x: g in x['genero'] and x['rating']).\
                map(lambda x: float(x['rating']))

            duration_genres = entities.\
                filter(lambda x: g in x['genero'] and x['rating']).\
                map(duration_transform).\
                filter(lambda x: x > 0)

            genre_stats[g] = {}

            try:
                genre_stats[g]['duration'] = {
                    'mean': duration_genres.mean(),
                    'std': duration_genres.std(),
                    'min': duration_genres.min(),
                    'max': duration_genres.max(),
                }
            except Exception:
                genre_stats[g]['duration'] = {
                    'mean': None,
                    'std': None,
                    'min': None,
                    'max': None,
                }

            try:
                genre_stats[g]['rates'] = {
                    'p(rate>8|genre)': rates_genre.prob(
                        lambda x: x >= 8,
                    ),
                    'mean': rates_genre.mean(),
                    'std': rates_genre.std(),
                    'min': rates_genre.min(),
                    'max': rates_genre.max(),
                }
            except Exception:
                genre_stats[g]['rates'] = {
                    'p(rate>8|genre)': None,
                    'mean': None,
                    'std': None,
                    'min': None,
                    'max': None,
                }

        self.write({
            'rates': rate_stats,
            'duration': duration_stats,
            'stats_by_genre': genre_stats,
        })


if __name__ == "__main__":
    db = MongoDB('mongodb://localhost:27017/')

    app = Application([
        ("/", DesciptionHandler, {'db': db}),
        ("/find", FindHandler, {'db': db}),
        ("/findall", FindAllHandler, {'db': db}),
        ("/stats", StatsHandler, {'db': db}),
    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
