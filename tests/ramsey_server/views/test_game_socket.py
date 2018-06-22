import json

import pytest
from aiohttp import WSMsgType

from ramsey_game.player import State
from ramsey_server.game_handlers.player import (
    MSG_CONNECT,
    MSG_INFO,
    MSG_GAME,
    MSG_MOVE,
    MSG_WON,
    MSG_ERROR,
)


def get_move_msg(start, end):
    return {
        'type': MSG_MOVE,
        'start_node': start,
        'end_node': end,
    }


async def assert_message(player, type):
    if isinstance(player, list):
        for player in player:
            message = (await player.receive(timeout=3)).json()
            assert message['type'] == type
    else:
        message = (await player.receive(timeout=3)).json()
        assert message['type'] == type


@pytest.fixture
async def player_1(client, started_game_id):
    ws = await client.ws_connect(f'/game/{started_game_id}')
    join_message = {'type': MSG_CONNECT}
    await ws.send_str(json.dumps(join_message))

    # get not enough players message
    await ws.receive(timeout=3)

    return ws


@pytest.fixture
async def player_2(player_1, client, started_game_id):
    ws = await client.ws_connect(f'/game/{started_game_id}')
    join_message = {'type': MSG_CONNECT}
    await ws.send_str(json.dumps(join_message))

    return ws


async def test_game_player_join_no_players(client, started_game_id):
    ws = await client.ws_connect(f'/game/{started_game_id}')

    join_message = {'type': MSG_CONNECT}
    await ws.send_str(json.dumps(join_message))

    message = (await ws.receive(timeout=3)).json()
    assert message['body']['details'] == 'NotEnoughPlayers()'
    assert message['type'] == MSG_INFO


async def test_player_join_and_disconnect(
        app, client, started_game_id, started_game, player_1
):
    await player_1.close()
    message = (await player_1.receive(timeout=3))

    assert message.type == WSMsgType.CLOSED
    assert len(app['games']) == 0


async def test_2_players_joins_game_starts(
        client, started_game_id, started_game, player_1, player_2
):
    message = (await player_2.receive(timeout=3)).json()
    assert message['type'] == MSG_GAME
    assert message['body']['available_graph']

    message = (await player_1.receive(timeout=3)).json()
    assert message['type'] == MSG_GAME
    assert message['body']['available_graph']

    assert started_game.player_manager.state == State.started


async def test_2_players_full_game_through_network(
        client, started_game_id, started_game, player_1, player_2
):
    # get game messages
    await assert_message([player_1, player_2], MSG_GAME)

    # first turn
    await player_1.send_str(json.dumps(get_move_msg(0, 1)))
    await assert_message([player_1, player_2], MSG_MOVE)
    await player_2.send_str(json.dumps(get_move_msg(3, 4)))
    await assert_message([player_1, player_2], MSG_MOVE)

    # second turn
    await player_1.send_str(json.dumps(get_move_msg(1, 2)))
    await assert_message([player_1, player_2], MSG_MOVE)
    await player_2.send_str(json.dumps(get_move_msg(4, 5)))
    await assert_message([player_1, player_2], MSG_MOVE)

    # winning move
    await player_1.send_str(json.dumps(get_move_msg(2, 0)))
    await assert_message([player_1, player_2], MSG_GAME)

    message_winning = (await player_1.receive(timeout=3)).json()
    message_loosing = (await player_2.receive(timeout=3)).json()

    assert message_winning['type'] == MSG_WON
    assert message_loosing['type'] == MSG_ERROR

    assert started_game
