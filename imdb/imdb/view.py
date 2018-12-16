import json

import tornado.ioloop
import tornado.web

from imdb.persistence import MongoDB
from imdb.numeric import StatVector

db = MongoDB('mongodb://localhost:27017/')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        
        objs = list(db.fetchall())
        for obj in objs:
            obj['_id'] = str(obj['_id'])
        
        self.write(json.dumps(objs))


class StatsHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        entities_list = []
        genres_list = set()

        for e in db.fetchall():
            if not e['rating']:
                continue

            genres_list |= set(e['genero'])
            e['rating'] = float(e['rating'])
            entities_list.append(e)

        rates = StatVector(
            float(e['rating']) for e in entities_list if e['rating']
        )

        entities = StatVector(entities_list)
        genre_stats = {}
        for g in genres_list:
            genre_stats[g] = {
                'p>8': entities.cond_prob(
                    lambda x: x['rating'] >= 8,
                    lambda x: g in x['genero']
                )
            }

        self.write({
            'rates': {
                'mean': rates.mean(),
                'std': rates.std(),
                'min': rates.min(),
                'max': rates.max(),
            },
            'no_rates': {
                'entries': [
                    e for e in entities_list if not(e['rating'])
                ],
                'count': len([
                    e for e in entities_list if not(e['rating'])
                ])
            },
            'rates_by_genre': genre_stats,
        })


def make_app():
    return tornado.web.Application([
        ("/", MainHandler),
        ("/stats", StatsHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
