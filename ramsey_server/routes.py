from ramsey_server.views.game_socket import GameSocket

routes = [
    ('GET', '/game/{room_id}', GameSocket, 'game'),
]
