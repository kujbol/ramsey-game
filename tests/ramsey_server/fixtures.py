import pytest

from ramsey_server.app import init


@pytest.fixture
async def app(loop):
    _, _, app = await init(loop)
    return app


@pytest.fixture
async def client(aiohttp_client, app):
    client = await aiohttp_client(app)
    return client


@pytest.fixture
def game_start_data():
    return {
        'data': {
            'graph_size': 7,
            'clique_size': 3,
            'game_name': 'test',
        }
    }


@pytest.fixture()
async def started_game_id(client, app, game_start_data):
    response = await client.post('/games', json=game_start_data)
    resp_json = await response.json()

    return resp_json['data']['room_id']


@pytest.fixture()
async def started_game(app, started_game_id):
    return app['games'][started_game_id]
