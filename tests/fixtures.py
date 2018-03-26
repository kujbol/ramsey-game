import pytest

from ramsey_game.game import GameGraph


@pytest.fixture
def raw_game():
    return GameGraph(5, 3)


@pytest.fixture()
def raw_short_game():
    return GameGraph(3, 3)


@pytest.fixture
def p1():
    return 'player_1'


@pytest.fixture
def p2():
    return 'player_2'


def start_game(game, p1, p2):
    game.add_player(p1)
    game.add_player(p2)
    game.start_game()
    return game


@pytest.fixture
def game(raw_game, p1, p2):
    return start_game(raw_game, p1, p2)


@pytest.fixture
def short_game(raw_short_game, p1, p2):
    return start_game(raw_short_game, p1, p2)