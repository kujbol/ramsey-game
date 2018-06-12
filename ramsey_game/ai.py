import random

from ramsey_game.game import GameGraph
from ramsey_game.player import Player, PlayerManager


class AIPlayer(Player):
    pass


class AIPlayerManager(PlayerManager):
    ai_player_id = 'ai-player'

    def __init__(self, size):
        super().__init__(size)
        self.players[self.ai_player_id] = AIPlayer(size)

    def start_game(self):
        super().start_game()
        self.actual_player = self.next_player()


class AIGameGraph(GameGraph):
    def __init__(self, size, finish_size, game_name='Test Game'):
        super().__init__(size, finish_size, game_name)
        self.player_manager = AIPlayerManager(size)

    def ai_move(self):
        edge = random.choice(list(self.graph.edges))
        super().move(edge[0], edge[1], self.player_manager.ai_player_id)
        return edge
