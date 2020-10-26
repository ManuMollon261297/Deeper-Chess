from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior

import chess
import manlioAI

#board = chess.Board('8/8/p7/p1K4r/p5r1/8/8/7k w - - 0 1')
board = chess.Board()

data_dir = 'data/'
image_dir = data_dir + 'images/'
cp_images = image_dir + 'chess-pieces/'
other_images = image_dir + 'other/'

pieceDir = dict({'p': cp_images + 'bp.png',
                 'r': cp_images + 'br.png',
                 'n': cp_images + 'bn.png',
                 'b': cp_images + 'bb.png',
                 'q': cp_images + 'bq.png',
                 'k': cp_images + 'bk.png',
                 'P': cp_images + 'wp.png',
                 'R': cp_images + 'wr.png',
                 'N': cp_images + 'wn.png',
                 'B': cp_images + 'wb.png',
                 'Q': cp_images + 'wq.png',
                 'K': cp_images + 'wk.png',})
squareLetter = dict({0: 'a',
                     1: 'b',
                     2: 'c',
                     3: 'd',
                     4: 'e',
                     5: 'f',
                     6: 'g',
                     7: 'h',})

class Chessboard(Widget):
    pass

class Square(ButtonBehavior, Image):
    def on_release(self):
        self.parent.moveString += self.id
        if len(self.parent.moveString) == 4:
            try:
                move = chess.Move.from_uci(self.parent.moveString)
                if move in board.legal_moves:
                    board.push(move)
                    self.parent.drawPieces(list(board.fen().split()[0]))
                    move = manlioAI.cpuMoves(board)
                    board.push(move)
                self.parent.drawPieces(list(board.fen().split()[0]))
            except ValueError:
                print('Invalid move!')
            self.parent.moveString = ''
    def updateSquare(self, piece):
        if piece != 't':
            self.source = pieceDir[piece]
        else:
            self.source = 'data/images/other/transparency.png'
        pass
    def set_square_id(self, idNr):
        number = int(idNr/8)+1
        letter = squareLetter[7-idNr%8]
        square = letter+str(number)
        self.id = square

class ChessSquares(GridLayout):
    moveString = ''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def drawPieces(self, data):
        square = 0
        pieces = list()
        for piece in data:
            if piece == '/':
                pass
            elif piece in pieceDir:
                pieces.append(piece)
            elif piece.isdigit():
                for i in range(int(piece)):
                    pieces.append('t')
        print(pieces.reverse())
        for chid in self.children:
            chid.updateSquare(pieces[square])
            square = square + 1
    def set_squares_ids(self):
        square = 0
        for chid in self.children:
            chid.set_square_id(square)
            square = square + 1


class ChessGame(Widget):
    def update_board(self, board):
        data = list(board.fen().split()[0])
        self.children[0].drawPieces(data)
    def set_ids(self):
        self.children[0].set_squares_ids()

class ChessApp(App):
    def build(self):
        Config.set('graphics', 'resizable', '1')
        Config.write()
        self.title = 'Manlio Chess AI'
        self.icon = 'manlioIconSmall.png'

        game = ChessGame()
        game.set_ids()
        game.update_board(board)

        Window.size = (700, 700)
        return game


if __name__ == '__main__':
    ChessApp().run()