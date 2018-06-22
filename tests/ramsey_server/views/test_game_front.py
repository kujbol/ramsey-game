async def test_game_front(client):
    resp = await client.get('/')

    assert resp.status == 200
