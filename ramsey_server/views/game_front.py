import aiohttp_jinja2
from aiohttp import web


class GameFront(web.View):
    @aiohttp_jinja2.template('index.html')
    def get(self):
        return {}
