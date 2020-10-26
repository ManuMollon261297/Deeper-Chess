import chess
import chess.svg
import IPython.display

class Game:
    def __init__(self):
        self.name = 'chess'
        self.currentPlayer = chess.WHITE
        self.gameState = GameState()
        self.result = '*'

    def reset(self):
        self.gameState = chess.Board()
        self.currentPlayer = chess.WHITE

    def step(self, action):
        self.gameState.takeAction(action)
        self.currentPlayer = not self.currentPlayer

class GameState():
    def __init__(self):
        self.board = chess.Board()
        self.id = self._convertStateToId()
        self.allowedActions = self._allowedActions()
        self.isEndGame = self._checkForEndGame()

    def _allowedActions(self):
        return self.board.legal_moves

    def _convertStateToId(self):
        return self.board.fen()

    def _checkForEndGame(self):
        return self.board.is_game_over(claim_draw=True)

    def takeAction(self, action):
        self.board.push(action)
        self.id = self._convertStateToId()
        self.allowedActions = self._allowedActions()
        self.isEndGame = self._checkForEndGame()

    def render(self):
        print(self.board)
        chess.svg.board(self.board)
