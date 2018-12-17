import logging
from urllib import parse

from imdb.models import Item, Request

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.imdb.com'

URL_GENRES = BASE_URL + '/feature/genre/'

XPATH_LINKS_GENRES = '/html/body//div[./span/span/h3/text()=" Popular Movies by Genre"]/div/div/div//a/@href'  # noqa

# noqua
XPATH_MOVIE_DETAILS = '/html/body//div/div/div/div[@class="lister-item-content"]'


def clear_url(url, base_url='', keep_args=[]):
    if base_url:
        url = parse.urljoin(base_url, url)

    parsed = parse.urlparse(url, allow_fragments=False)
    url_args = parse.parse_qs(parsed.query)
    query = '&'.join('{}={}'.format(k, v[0])
                     for k, v in url_args.items() if k in keep_args)

    parsed = parse.ParseResult(parsed.scheme,
                               parsed.netloc,
                               parsed.path,
                               parsed.params,
                               query,
                               parsed.fragment)

    return parsed.geturl()


class IMDBSpider():
    base_url = BASE_URL
    start_url = URL_GENRES

    def __init__(self, paginacao=1):
        self.paginacao = paginacao

    def start_requests(self):
        return [Request(self.start_url, self.parse_genres)]

    def parse_genres(self, response):
        logger.info('Processando {}'.format(response.url))
        links = response.xpath(XPATH_LINKS_GENRES).extract()
        for link in links:
            logger.info('')
            link = clear_url(link, self.base_url, ('genres', 'title_type'))
            link += '&sort=num_votes,desc'
            for page in range(self.paginacao):
                ulink = '{}&start={}'.format(link, 1 + 50*page)
                yield Request(ulink, self.parse_movies)

    def parse_movies(self, response):
        logger.info('Processando {}'.format(response.url))
        for movie_selector in response.xpath(XPATH_MOVIE_DETAILS):
            titulo = movie_selector.xpath('./h3/a/text()').extract_first()

            url = movie_selector.xpath('./h3/a/@href').extract_first()
            url = clear_url(url, self.base_url)

            rating = movie_selector.xpath(
                './/div/div[@class="inline-block ratings-imdb-rating"]/@data-value').extract_first()

            genres = movie_selector.xpath(
                './p[@class="text-muted "]/span[@class="genre"]/text()').extract_first().split(',')
            genres = [g.strip() for g in genres]

            duracao = movie_selector.xpath(
                './p[@class="text-muted "]/span[@class="runtime"]/text()').re('(\d+) min')

            if duracao:
                duracao = duracao[0]
            else:
                duracao = None

            nodes = movie_selector.xpath('./p[@class=""]/node()')
            directors = []
            stars = []
            coll = []
            while nodes:
                node = nodes.pop(0)
                if node.re('Direct'):
                    coll = directors
                if node.re('Stars'):
                    coll = stars
                elif node.xpath('./@href'):
                    subitem = {
                        'url': BASE_URL + node.xpath('./@href').extract_first(),
                        'name': node.xpath('./text()').extract_first(),
                    }
                    subitem['url'] = clear_url(subitem['url'], self.base_url)
                    coll.append(subitem)

            movie = {
                'url_origem': response.url,
                'url': url,
                'titulo': titulo,
                'rating': rating,
                'diretores': directors,
                'estrelas': stars,
                'genero': genres,
                'duracao': duracao,
                '_raw': movie_selector.extract()
            }

            logger.info('Extratido item em {}'.format(movie['url']))
            yield Item(movie)
