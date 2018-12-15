from pprint import pprint

from parsel import Selector

from imdb.engine import RequestsEngine
from imdb.spider import IMDBSpider


def add_selector(response):
    selector = Selector(text=response.text)
    setattr(response, 'selector', selector)
    setattr(response, 'xpath', selector.xpath)
    return response

def print_item(item):
    pprint(item)
    return item


if __name__ == '__main__':
    spider = IMDBSpider()
    engine = RequestsEngine(spider.start_request())

    engine.add_response_hook(add_selector)
    engine.add_item_hook(print_item)

    engine.run()