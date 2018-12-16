from imdb.constants import (URL_GENRES, BASE_URL,
                            XPATH_LINKS_GENRES,
                            XPATH_MOVIE_DETAILS)

from imdb.models import Item, Request


class IMDBSpider():
    def start_requests(self):
        return [Request(URL_GENRES, self.parse_genres)]

    def parse_genres(self, response):
        links = response.xpath(XPATH_LINKS_GENRES).extract()
        for link in links:
            yield Request(BASE_URL + link,
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

            url = movie_selector.xpath('./h3/a/@href').extract_first()

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
                        'url': node.xpath('./@href').extract_first(),
                        'name': node.xpath('./text()').extract_first(),
                    })

            movie = {
                'url': url,
                'titulo': titulo,
                'rating': rating,
                'diretores': directors,
                'estrelas': stars,
                'genero': genres,
                'duracao': duracao,
            }

            yield Item(movie)
