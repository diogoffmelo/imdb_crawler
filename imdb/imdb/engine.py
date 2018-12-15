from collections import deque

import requests

from imdb.models import Request, Item


class RequestsEngine(object):
    """
    Main request scheduler

    Generate and dispatche requests generated by parsers.
    Hooks can be setted do responses and Items. 
    """
    def __init__(self, startRequest):
        self.queue = deque()
        self.queue.append(startRequest)
        self.visited = set()
        self.item_hooks = []
        self.response_hooks = []

    def add_item_hook(self, hook):
        """Register a hook to items"""
        self.item_hooks.append(hook)

    def add_response_hook(self, hook):
        """Register a hook to responses"""
        self.response_hooks.append(hook)

    def run(self):
        while self.queue:
            request = self.queue.pop()
            self.visited.add(request)

            response = requests.get(request.url)
            for hook in self.response_hooks:
                response = hook(response)

            for crop in request.callback(response):
                if isinstance(crop, Item):
                    for hook in self.item_hooks:
                        crop = hook(crop)
                
                elif isinstance(crop, Request):
                    if crop not in self.visited:
                        self.queue.append(crop)
