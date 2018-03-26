import pytest

from ramsey_game.exceptions import InvalidMove, InvalidTurn, PlayerWon, Draw


def test_game_won(game, p1, p2):
    game.move(0, 1, p1)
    game.move(3, 4, p2)
    game.move(1, 2, p1)
    game.move(1, 4, p2)

    with pytest.raises(PlayerWon) as exc:
        game.move(2, 0, p1)

    assert exc.value.args[0] == p1


def test_game_draw(short_game, p1, p2):
    short_game.move(0, 1, p1)
    short_game.move(1, 2, p2)
    with pytest.raises(Draw):
        short_game.move(0, 2, p1)


def test_game_invalid_move(game, p1, p2):
    game.move(0, 1, p1)

    with pytest.raises(InvalidMove):
        game.move(0, 1, p2)


def test_game_cheating_move(game, p1):
    game.move(0, 1, p1)
    with pytest.raises(InvalidTurn):
        game.move(1, 2, p1)


def test_game_cheating_move_and_draw(short_game, p1, p2):
    short_game.move(0, 1, p1)
    with pytest.raises(InvalidTurn):
        short_game.move(1, 2, p1)

    short_game.move(1, 2, p2)
    with pytest.raises(Draw):
        short_game.move(0, 2, p1)
