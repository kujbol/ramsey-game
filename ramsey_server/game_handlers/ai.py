from ramsey_server.game_handlers.player import GameHandler, MSG_MOVE, message


class AIGameHandler(GameHandler):
    async def make_move(self, msg_json):
        await super().make_move(msg_json)

        move_edge = self.game.ai_move()
        move_response = {
            'start_node': move_edge[0],
            'end_node': move_edge[1],
        }

        for _ws in self.room:
            ai_player_id = self.game.player_manager.ai_player_id
            await _ws.send_json(
                message(MSG_MOVE, move_response, ai_player_id)
            )
