from ramsey_server.views.game_socket import GameSocket
from ramsey_server.views.auth import Login

routes = [
    ('GET', '/game/{room_id}', GameSocket, 'game'),
]
