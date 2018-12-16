import json


DBSETTING = '../movies.json'


class DBConn():
    def __init__(self):
        self.items = []

    def persist(self, item):
        self.items.append(item)
        with open(DBSETTING, 'w') as f:
            json.dump(self.items, f)

        return item

    def fetchall(self):
        with open(DBSETTING, 'r') as f:
            self.items = json.load(f)

        return self.items

    def close(self):
        pass
