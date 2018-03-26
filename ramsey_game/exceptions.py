class InvalidMove(Exception):
    pass


class InvalidTurn(Exception):
    pass


class EndGame(Exception):
    pass


class PlayerWon(EndGame):
    pass


class Draw(EndGame):
    pass


class GameStarted(Exception):
    pass


class GameNotStartedYet(Exception):
    pass