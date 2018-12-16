from pprint import pprint

from parsel import Selector

from imdb.engine import RequestsEngine
from imdb.spider import IMDBSpider
from imdb.persistence import DBConn


def add_selector(response):
    selector = Selector(text=response.text)
    setattr(response, 'selector', selector)
    setattr(response, 'xpath', selector.xpath)
    return response


def print_item(item):
    pprint(item)
    return item


if __name__ == '__main__':
    db = DBConn()
    spider = IMDBSpider()
    engine = RequestsEngine(spider.start_requests())

    engine.add_response_hook(add_selector)
    engine.add_item_hook(print_item)
    engine.add_item_hook(db.persist)

    engine.run()
