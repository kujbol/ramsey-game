import uuid

from aiohttp import web, WSMsgType

from ramsey_game.ai import AIGameGraph
from ramsey_server.game_handlers.ai import AIGameHandler
from ramsey_server.game_handlers.player import GameHandler, MSG_ERROR, message
from ramsey_server.settings import log


class GameSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        room_id = self.request.match_info['room_id']
        player = await self.get_player()

        log.debug(f'New player: {player} joined room: {room_id}')

        room = await self.get_room(room_id)
        game = await self.get_game(room_id)
        ws.player_id = player

        if game is None or room is None:
            await ws.send_json(
                message(MSG_ERROR, {'details': 'Game not initialized'}, player)
            )
            await ws.close()
            return ws

        room.append(ws)

        if isinstance(game, AIGameGraph):
            game_handler = AIGameHandler(game, room, player)
        else:
            game_handler = GameHandler(game, room, player)

        async for msg in ws:
            if msg.type == WSMsgType.text:
                log.debug(f'Received message: {msg.data}')
                await game_handler.handle_message(ws, msg)

            elif msg.type == WSMsgType.error:
                log.debug(f'Exception in connection{ws.exception()}')
                break
            else:
                log.debug(f'Unknown message type:{msg.data} closing connection')
                break

        room.remove(ws)

        for _ws in room:
            await _ws.close()

        self.delete_room(room_id)
        self.delete_game(room_id)

        log.debug('websocket connection closed')

        return ws

    async def get_player(self):
        # session = await get_session(self.request)
        # return session.get('player')
        return uuid.uuid4()

    async def get_room(self, room_id):
        room = self.request.app['rooms'].get(room_id)
        return room

    async def get_game(self, room_id):
        game = self.request.app['games'].get(room_id)
        return game

    def delete_room(self, room_id):
        self.request.app['rooms'].pop(room_id, None)

    def delete_game(self, room_id):
        self.request.app['games'].pop(room_id, None)


