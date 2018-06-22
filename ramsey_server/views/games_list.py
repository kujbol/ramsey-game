import aiohttp_cors as aiohttp_cors
from aiohttp import web


class GameList(web.View, aiohttp_cors.CorsViewMixin):
    async def get(self):
        games = self.request.app['games']

        response = {
            "data": {
                "games": [
                    game.dumps_preview(game_id)
                    for game_id, game in games.items()
                ]
            }
        }
        return web.json_response(response)
