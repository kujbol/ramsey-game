import uuid

from aiohttp import web, WSMsgType
from aiohttp_session import get_session

from ramsey_game.exceptions import (
    NotEnoughPlayers,
    GameException,
    EndGame,
    PlayerWon,
    Draw
)
from ramsey_server.settings import log


MSG_MOVE = 'MSG_MOVE'
MSG_GAME = 'MSG_GAME'
MSG_ERROR = 'MSG_ERROR'
MSG_INFO = 'MSG_INFO'
MSG_WON = 'MSG_WON'
MSG_CONNECT = 'MSG_CONNECT'


def message(msg_type, body, player):
    return {
        'type': msg_type,
        'body': body,
        'player': str(player)
    }


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


class GameHandler:
    def __init__(self, game, room, player):
        self.game = game
        self.room = room
        self.player = player

    async def handle_message(self, ws, msg):
        msg_json = msg.json()

        if msg_json['type'] == MSG_CONNECT:
            log.debug('Player joined, adding and trying to start game')
            try:
                self.game.add_player(self.player)
                self.game.start_game()
            except NotEnoughPlayers as exc:
                await ws.send_json(
                    message(MSG_INFO, {'details': repr(exc)}, self.player)
                )
                return
            except GameException as exc:
                await ws.send_json(
                    message(MSG_ERROR, {'details': repr(exc)}, self.player)
                )
                return

            log.debug('Game started, sending state')
            for _ws in self.room:
                await _ws.send_json(message(MSG_GAME, self.game.dumps(), None))
            return

        if msg_json['type'] == MSG_MOVE:
            log.debug('Received move message')
            try:
                self.game.move(
                    msg_json['start_node'], msg_json['end_node'], self.player
                )
                for _ws in self.room:
                    await _ws.send_json(
                        message(MSG_GAME, self.game.dumps(), None)
                    )
            except EndGame as exc:
                for _ws in self.room:
                    await _ws.send_json(
                        message(MSG_GAME, self.game.dumps(), None)
                    )

                    if isinstance(exc, PlayerWon):
                        if exc.args[0] == _ws.player_id:
                            await _ws.send_json(
                                message(MSG_WON, {'details': 'You Won!'}, None)
                            )
                        else:
                            await _ws.send_json(
                                message(MSG_ERROR, {'details': 'You Lose!'}, None)
                            )
                    elif isinstance(exc, Draw):
                        await _ws.send_json(
                            message(MSG_INFO, {'details': 'Draw!!'}, None)
                        )

                # close other connections first
                filtered_room = [_ws for _ws in self.room if _ws != ws]
                for _ws in filtered_room:
                    await _ws.close()

                await ws.close()

            except GameException as exc:
                await ws.send_json(
                    message(MSG_ERROR, {'details': repr(exc)}, self.player)
                )
