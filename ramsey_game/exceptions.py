class GameException(Exception):
    pass


class InvalidMove(GameException):
    pass


class InvalidTurn(GameException):
    pass


class GameStarted(GameException):
    pass


class GameNotStartedYet(GameException):
    pass


class NotEnoughPlayers(GameException):
    pass


class PlayerAlreadyInGame(GameException):
    pass


class EndGame(GameException):
    pass


class PlayerWon(EndGame):
    pass


class Draw(EndGame):
    pass
