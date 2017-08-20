
from chess_engine.chess_classes import ChessBoard


class ChessGame:
    def __init__(self, game_data):
        color_set = ChessBoard.BoardColorSet(checkerboard={'white': '#bbb', 'black': '#888'})
        self.board = ChessBoard.Board(color_set=color_set)
        if game_data:
            self.board.load_grid(game_data)
        # else:
        #     self.board.load_new_grid()
        #     self.board.save_grid()
