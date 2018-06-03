from ramsey_server.views.game_socket import GameSocket
from ramsey_server.views.game_start import GameStart
from ramsey_server.views.games_list import GameList

routes = [
    ('GET', '/game/{room_id}', GameSocket, 'game'),
    ('GET', '/games', GameList, 'game_list'),
    ('POST', '/games', GameStart, 'game_start'),
]
