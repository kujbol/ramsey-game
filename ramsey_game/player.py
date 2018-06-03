import enum
from itertools import cycle

import networkx
from networkx.readwrite import json_graph

from ramsey_game.exceptions import (
    GameStarted,
    GameNotStartedYet,
    NotEnoughPlayers,
    InvalidTurn,
    PlayerAlreadyInGame,
)


class State(enum.Enum):
    not_started = 1
    started = 2


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
        self.state = State.not_started

    def add_player(self, player_id):
        if len(self.players) == 2:
            raise GameStarted

        if player_id in self.players:
            raise PlayerAlreadyInGame

        self.players[player_id] = Player(self.size)
        self.players_list.append(player_id)

    def start_game(self):
        if self.player_count() != 2:
            raise NotEnoughPlayers

        self.state = State.started
        self.players_cycle = cycle(self.players.keys())
        self.actual_player = self.next_player()

    def __getitem__(self, item):
        return self.players[item]

    def move_player(self, player_id):
        if self.state == State.not_started:
            raise GameNotStartedYet

        if self.actual_player != player_id:
            raise InvalidTurn(player_id)

        self.actual_player = self.next_player()

    def next_player(self):
        return next(self.players_cycle)

    def dumps(self):
        if self.state == State.not_started:
            raise GameNotStartedYet

        return {
            str(player_id): json_graph.node_link_data(player.graph)
            for player_id, player in self.players.items()
        }

    def player_count(self):
        return len(self.players)
