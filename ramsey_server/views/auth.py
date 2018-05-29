import uuid

from aiohttp import web
from aiohttp_session import get_session


class Login(web.View):
    async def get(self):
        session = await get_session(self.request)
        if session.get('player'):
            session['player'] = uuid.uuid4()

        return web.Response(status=200, body='success')
