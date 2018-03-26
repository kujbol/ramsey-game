import networkx

from ramsey_game.exceptions import (
    InvalidMove,
    PlayerWon,
    Draw,
)
from ramsey_game.player import PlayerManager


class GameGraph:
    # TODO game should start with initialized player manager
    def __init__(self, size, finish_size):
        self.finish_size = finish_size
        self.size = size
        
        self.graph = networkx.complete_graph(size)
        self.player_manager = PlayerManager(size)

    def add_player(self, player_id):
        self.player_manager.add_player(player_id)

    def start_game(self):
        self.player_manager.start_game()

    def move(self, u, v, player_id):
        self.player_manager.move_player(player_id)
        self.delete_available_move(player_id, u, v)

        move_result = self.player_manager[player_id].move(u, v)

        self.check_winning(move_result, player_id)

    def delete_available_move(self, player_id, u, v):
        try:
            self.graph.remove_edge(u, v)
        except networkx.NetworkXError:
            raise InvalidMove(u, v, player_id)
        
    def check_winning(self, move_result, player_id):
        if move_result >= self.finish_size:
            raise PlayerWon(player_id)

        if self.graph.size() == 0:
            raise Draw()
