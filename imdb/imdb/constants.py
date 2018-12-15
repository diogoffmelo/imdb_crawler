
BASE_URL = 'https://www.imdb.com'

URL_GENRES = BASE_URL + '/feature/genre/'

XPATH_LINKS_GENRES = '/html/body//div[./span/span/h3/text()=" Popular Movies by Genre"]/div/div/div//a/@href' # noqa

XPATH_MOVIE_DETAILS = '/html/body//div/div/div/div[@class="lister-item-content"]' # noqua