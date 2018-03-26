from itertools import cycle

import networkx

from ramsey_game.exceptions import GameStarted, GameNotStartedYet, InvalidTurn


class Player:
    def __init__(self, size):
        self.graph = networkx.empty_graph(size)

    def move(self, u, v):
        self.graph.add_edge(u, v)
        return networkx.graph_clique_number(self.graph)


class PlayerManager:
    def __init__(self, size):
        self.size = size
        self.players = {}
        self.players_list = []
        self.players_cycle = None
        self.actual_player = None

    def add_player(self, player_id):
        if len(self.players) == 2:
            raise GameStarted

        if player_id in self.players:
            raise GameStarted

        self.players[player_id] = Player(self.size)
        self.players_list.append(player_id)

    def start_game(self):
        self.players_cycle = cycle(self.players.keys())
        self.actual_player = self.next_player()

    def __getitem__(self, item):
        return self.players[item]

    def move_player(self, player_id):
        if not self.players_cycle:
            raise GameNotStartedYet

        if self.actual_player != player_id:
            raise InvalidTurn(player_id)

        self.actual_player = self.next_player()

    def next_player(self):
        return next(self.players_cycle)
