import aiohttp_cors as aiohttp_cors
from aiohttp import web

from ramsey_game.game import GameGraph
from ramsey_game.ai import AIGameGraph


class GameStart(web.View, aiohttp_cors.CorsViewMixin):
    async def post(self):
        body = await self.request.json()
        data = body['data']
        room_id = None

        for i in range(1000):
            if not self.request.app['games'].get(str(i)):
                room_id = str(i)
                break

        game = self.create_game(data)

        self.request.app['games'][room_id] = game
        self.request.app['rooms'][room_id] = []

        return web.json_response({"data": {"room_id": room_id}})

    def create_game(self, data):
        if data.get('is_ai'):
            return AIGameGraph(
                int(data['graph_size']), int(data['clique_size']),
                game_name=data['game_name']
            )
        else:
            return GameGraph(
                int(data['graph_size']), int(data['clique_size']),
                game_name=data['game_name']
            )
