import pymongo
import json


class DBConn():
    def __init__(self, url):
        self.url = url

    def persist(self):
        raise NotImplementedError()

    def fetchall(self):
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
        item = self.filmes.update(
            {'url': item['url']}, 
            item,
            upsert=True
        )
        return item

    def fetchall(self):
        return self.filmes.find()

    def close(self):
        pass


class JsonFile(DBConn):
    def __init__(self, url):
        DBConn.__init__(self, url)
        self.items = []

    def persist(self, item):
        self.items.append(item)
        with open(self.url, 'w') as f:
            json.dump(self.items, f)

        return item

    def fetchall(self):
        with open(self.url, 'r') as f:
            self.items = json.load(f)

        return self.items

    def close(self):
        pass
