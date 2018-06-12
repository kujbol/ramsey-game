from ramsey_game.exceptions import (
    EndGame,
    PlayerWon,
    Draw,
    GameException,
    NotEnoughPlayers
)
from ramsey_server.settings import log


class GameHandler:
    def __init__(self, game, room, player):
        self.game = game
        self.room = room
        self.player = player

    async def handle_message(self, ws, msg):
        msg_json = msg.json()

        if msg_json['type'] == MSG_CONNECT:
            await self.handle_connect(ws)

        if msg_json['type'] == MSG_MOVE:
            await self.handle_move(msg_json, ws)

    async def handle_move(self, msg_json, ws):
        log.debug('Received move message')
        try:
            await self.make_move(msg_json)
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

    async def make_move(self, msg_json):
        self.game.move(
            msg_json['start_node'], msg_json['end_node'], self.player
        )
        for _ws in self.room:
            await _ws.send_json(
                message(MSG_MOVE, msg_json, self.player)
            )

    async def handle_connect(self, ws):
        log.debug('Player joined, adding and trying to start game')
        try:
            self.game.add_player(self.player)
            self.game.start_game()
        except NotEnoughPlayers as exc:
            await ws.send_json(
                message(MSG_INFO, {'details': repr(exc)}, self.player)
            )
        except GameException as exc:
            await ws.send_json(
                message(MSG_ERROR, {'details': repr(exc)}, self.player)
            )
        else:
            log.debug('Game started, sending state')
            for _ws in self.room:
                await _ws.send_json(
                    message(MSG_GAME, self.game.dumps(), None)
                )


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
