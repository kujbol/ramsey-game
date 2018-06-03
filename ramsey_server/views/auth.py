import uuid

import aiohttp_cors
from aiohttp import web
from aiohttp_session import get_session


class Login(web.View, aiohttp_cors.CorsViewMixin):
    async def post(self):
        session = await get_session(self.request)
        player_id = session.get('player')
        if not player_id:
            player_id = uuid.uuid4()
            session['player'] = str(player_id)

        return web.json_response({'data': {'user_id': str(player_id)}})
