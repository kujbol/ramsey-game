import pytest

from ramsey_game.ai import AIGameGraph
from ramsey_game.game import GameGraph


@pytest.mark.parametrize('param_is_ai', [True, False])
async def test_game_start(client, game_start_data, param_is_ai, app):
    game_start_data['data']['is_ai'] = param_is_ai

    response = await client.post('/games', json=game_start_data)
    data = (await response.json())['data']

    # this will be always first room
    assert data['room_id'] == '0'

    assert app['rooms']['0'] == []
    game = app['games']['0']

    assert game.finish_size == game_start_data['data']['clique_size']
    assert game.size == game_start_data['data']['graph_size']
    assert game.name == game_start_data['data']['game_name']

    if param_is_ai:
        assert isinstance(game, AIGameGraph)
    else:
        assert isinstance(game, GameGraph)


async def test_game_start_when_one_started(
        client, game_start_data, started_game
):
    response = await client.post('/games', json=game_start_data)
    assert response.status == 200
