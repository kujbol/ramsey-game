import aiohttp_cors as aiohttp_cors
from aiohttp import web


class GameList(web.View, aiohttp_cors.CorsViewMixin):
    async def get(self):
        games = self.request.app['games']

        response = {
            "data": {
                "games": [
                    {
                        'id': game_id,
                        'name': game.name,
                        'size': game.size,
                        'finish_size': game.finish_size,
                        'expected_players': 2,
                        'player_count': game.player_manager.player_count(),
                        'state': game.player_manager.state.name
                    }
                    for game_id, game in games.items()
                ]
            }
        }
        return web.json_response(response)
