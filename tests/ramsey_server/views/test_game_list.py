async def test_list_games_no_games(client):
    response = await client.get('/games')
    assert response.status == 200

    data = await response.json()
    assert data['data']['games'] == []


async def test_list_games_one_game(client, started_game):
    response = await client.get('/games')
    assert response.status == 200

    data = await response.json()
    assert data['data']['games'][0] == started_game.dumps_preview('0')
    assert len(data['data']['games']) == 1
