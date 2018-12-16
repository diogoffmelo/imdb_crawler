from imdb.models import Item, Request

BASE_URL = 'https://www.imdb.com'

URL_GENRES = BASE_URL + '/feature/genre/'

XPATH_LINKS_GENRES = '/html/body//div[./span/span/h3/text()=" Popular Movies by Genre"]/div/div/div//a/@href'  # noqa

XPATH_MOVIE_DETAILS = '/html/body//div/div/div/div[@class="lister-item-content"]' # noqua


class IMDBSpider():
    base_url = BASE_URL
    start_url = URL_GENRES

    def start_requests(self):
        return [Request(self.start_url, self.parse_genres)]

    def parse_genres(self, response):
        links = response.xpath(XPATH_LINKS_GENRES).extract()
        for link in links:
            yield Request(self.base_url + link,
                          self.parse_movies_list)

    def parse_movies_list(self, response):
        for movie_selector in response.xpath(XPATH_MOVIE_DETAILS):

            # validação.....
            # status = movie_selector.xpath('./p[@class="text-muted "]/b/text()').extract_first()
            # if status in ['Filming', 'Post-production']:
            #     continue

            # import re
            # ano = movie_selector.xpath('./h3/span[@class="lister-item-year text-muted unbold"]/text()').extract_first()
            # if not ano:
            #    continue

            # ano = int(re.search('\d+', ano).group(0))
            # if ano > 2018:
            #     continue

            # if 'The Limit' in titulo:
            #     import ipdb; ipdb.set_trace()

            # titulo
            titulo = movie_selector.xpath('./h3/a/text()').extract_first()

            url = BASE_URL + movie_selector.xpath('./h3/a/@href').extract_first()

            # rating
            rating = movie_selector.xpath(
                './/div/div[@class="inline-block ratings-imdb-rating"]/@data-value').extract_first()

            genres = movie_selector.xpath(
                './p[@class="text-muted "]/span[@class="genre"]/text()').extract_first().split(',')

            duracao = movie_selector.xpath(
                './p[@class="text-muted "]/span[@class="runtime"]/text()').extract_first()

            nodes = movie_selector.xpath('./p[@class=""]/node()')
            nodes[0].re('Direct')
            nodes.pop(0)
            directors = []
            stars = []
            coll = directors
            while nodes:
                node = nodes.pop(0)
                if node.re('Stars'):
                    coll = stars
                elif node.xpath('./@href'):
                    coll.append({
                        'url': BASE_URL + node.xpath('./@href').extract_first(),
                        'name': node.xpath('./text()').extract_first(),
                    })

            movie = {
                'url_origem': response.url,
                'url': url,
                'titulo': titulo,
                'rating': rating,
                'diretores': directors,
                'estrelas': stars,
                'genero': genres,
                'duracao': duracao,
            }

            yield Item(movie)
