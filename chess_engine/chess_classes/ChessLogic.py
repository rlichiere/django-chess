
from chess_engine.chess_classes import ChessBoard
from utils import utils


class ChessGame:
    def __init__(self, game_data):
        color_set = ChessBoard.BoardColorSet(checkerboard={'white': '#bbb', 'black': '#888'})
        self.board = ChessBoard.Board(color_set=color_set)
        if game_data:
            self.board.load_grid(game_data)
        if not game_data.get_data('token/step/name'):
            game_data.set_data('token/step/name', 'waitCellSource')
