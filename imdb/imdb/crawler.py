from pprint import pprint

from imdb.engine import RequestsEngine
from imdb.spider import IMDBSpider
from imdb.persistence import MongoDB


def print_item(item):
    pprint({k: v for k, v in item.items() if k[0] != '_'})
    return item


if __name__ == '__main__':
    db = MongoDB('mongodb://localhost:27017/')
    spider = IMDBSpider(pagination=1)
    engine = RequestsEngine(spider.start_requests())

    engine.add_item_hook(print_item)
    engine.add_item_hook(db.persist)

    engine.run()
