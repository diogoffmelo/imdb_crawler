import json
from urllib import parse
import logging

import pymongo


logger = logging.getLogger(__name__)


class DBManager():
    @staticmethod
    def getConnection(url):
        logger.info('Configurando banco de dados...')

        parsed = parse.urlparse(url)
        if parsed.scheme == 'mongodb':
            db = MongoDB(url)
        elif parsed.scheme == 'json':
            db = JsonFile(parsed.netloc + parsed.path)
        else:
            raise Exception('Banco de dados não suportado.')

        logger.info('Banco de dados configurado...')
        return db


class DBConn():
    def __init__(self, url):
        self.url = url
        self.seen = set()

    def persist(self):
        raise NotImplementedError()

    def fetchall(self):
        raise NotImplementedError()

    def count(self):
        raise NotImplementedError()

    def find(self, skip=0, limit=50):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class MongoDB(DBConn):
    def __init__(self, url):
        DBConn.__init__(self, url)
        self.cli = pymongo.MongoClient(self.url)
        self.db = self.cli['imdb']
        self.filmes = self.db['filmes']
        self.filmes.create_index(
            [('url', pymongo.TEXT)],
        )

    def persist(self, item):
        if item['url'] not in self.seen:
            self.seen.add(item['url'])
            self.filmes.update(
                {'url': item['url']},
                item,
                upsert=True
            )
        return item

    def fetchall(self):
        return self.filmes.find()

    def find(self, skip=0, limit=50):
        return self.filmes.find(skip=skip, limit=limit)

    def count(self):
        return self.filmes.count()

    def close(self):
        pass


class JsonFile(DBConn):
    def __init__(self, url):
        DBConn.__init__(self, url)
        self.filmes = []

    def persist(self, item):
        if item['url'] not in self.seen:
            self.seen.add(item['url'])
            item['_id'] = str(len(self.seen))
            self.filmes.append(item)
            with open(self.url, 'w') as f:
                json.dump(self.filmes, f)

        return item

    def fetchall(self):
        with open(self.url, 'r') as f:
            self.filmes = json.load(f)
            for item in self.filmes:
                self.seen.add(item['url'])

        return self.filmes

    def find(self, skip=0, limit=50):
        self.fetchall(self)
        return self.filmes[skip:min(len(self.filmes), skip+limit)]

    def count(self):
        self.fetchall(self)
        return len(self.filmes)

    def close(self):
        pass
