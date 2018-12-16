
class Request():
    def __init__(self, url, callback):
        self.url = url
        self.callback = callback

    def __hash__(self):
        return hash(self.url)


class Item(dict):
    pass
