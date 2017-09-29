
from django.template import loader

from chess_engine.chess_classes import ChessPiece
from chess_engine.models import GamePersistentData
from utils import utils


class Side:
    def __init__(self, name):
        self.name = name
        self.pieces = list()


class BoardColorSet:
    def __init__(self, checkerboard):
        self.checkerboard = checkerboard
        self.source_piece = '#559'
        self.target_piece = '#595'


class Board:
    template_name = 'chess_engine/board.html'

    def __init__(self):
        print 'ChessBoard.__init__'
        self.grid = dict()
        self.game_data = None
        self.sides = dict()
        self.sides['white'] = Side('white')
        self.sides['black'] = Side('black')

        self.default_color_set = BoardColorSet(checkerboard={'white': '#bbb', 'black': '#888'})
        self.color_set = self.default_color_set

    def set_color_set(self, color_set):
        self.color_set = color_set

    def load_grid(self, game_data):
        self.game_data = game_data
        loaded_grid = self.game_data.get_data('board')
        if not loaded_grid:
            print 'Board.load_grid: unfound data, so create new one.'
            self.load_new_grid()
            self.save_grid()
            print 'Board.load_grid: created.'
        else:
            # build Pieces from data
            for line_key in loaded_grid:
                line = loaded_grid[line_key]
                for cell_key in line:
                    cell = line[cell_key]
                    if cell == '-':
                        utils.access(self.grid, '%s/%s' % (line_key, cell_key), '-')
                    else:
                        if cell['s'] == 'w':
                            side = self.sides['white']
                        else:
                            side = self.sides['black']

                        if cell['r'] == 'P':
                            piece = ChessPiece.PiecePawn(self, cell['n'], side)
                        elif cell['r'] == 'R':
                            piece = ChessPiece.PieceRook(self, cell['n'], side)
                        elif cell['r'] == 'H':
                            piece = ChessPiece.PieceHorse(self, cell['n'], side)
                        elif cell['r'] == 'B':
                            piece = ChessPiece.PieceBishop(self, cell['n'], side)
                        elif cell['r'] == 'Q':
                            piece = ChessPiece.PieceQueen(self, cell['n'], side)
                        elif cell['r'] == 'K':
                            piece = ChessPiece.PieceKing(self, cell['n'], side)
                        utils.access(self.grid, '%s/%s' % (line_key, cell_key), piece)
            print 'Board.load_grid: loaded.'

    def save_grid(self):
        self.game_data.set_data('board', self.grid)
        print 'Board.save_grid: saved.'

    def load_new_grid(self):
        whites = Side('white')
        wp1 = ChessPiece.PiecePawn(self, 'p1', whites)
        whites.pieces.append(wp1)
        wp2 = ChessPiece.PiecePawn(self, 'p2', whites)
        whites.pieces.append(wp2)
        wp3 = ChessPiece.PiecePawn(self, 'p3', whites)
        whites.pieces.append(wp3)
        wp4 = ChessPiece.PiecePawn(self, 'p4', whites)
        whites.pieces.append(wp4)
        wp5 = ChessPiece.PiecePawn(self, 'p5', whites)
        whites.pieces.append(wp5)
        wp6 = ChessPiece.PiecePawn(self, 'p6', whites)
        whites.pieces.append(wp6)
        wp7 = ChessPiece.PiecePawn(self, 'p7', whites)
        whites.pieces.append(wp7)
        wp8 = ChessPiece.PiecePawn(self, 'p8', whites)
        whites.pieces.append(wp8)
        wr1 = ChessPiece.PieceRook(self, 'r1', whites)
        whites.pieces.append(wr1)
        wh1 = ChessPiece.PieceHorse(self, 'h1', whites)
        whites.pieces.append(wh1)
        wb1 = ChessPiece.PieceBishop(self, 'b1', whites)
        whites.pieces.append(wb1)
        wq = ChessPiece.PieceQueen(self, 'q', whites)
        whites.pieces.append(wq)
        wk = ChessPiece.PieceKing(self, 'k', whites)
        whites.pieces.append(wk)
        wb2 = ChessPiece.PieceBishop(self, 'b2', whites)
        whites.pieces.append(wb2)
        wh2 = ChessPiece.PieceHorse(self, 'h2', whites)
        whites.pieces.append(wh2)
        wr2 = ChessPiece.PieceRook(self, 'r2', whites)
        whites.pieces.append(wr2)
        self.sides['white'] = whites

        blacks = Side('black')
        bp1 = ChessPiece.PiecePawn(self, 'p1', blacks)
        blacks.pieces.append(bp1)
        bp2 = ChessPiece.PiecePawn(self, 'p2', blacks)
        blacks.pieces.append(bp2)
        bp3 = ChessPiece.PiecePawn(self, 'p3', blacks)
        blacks.pieces.append(bp3)
        bp4 = ChessPiece.PiecePawn(self, 'p4', blacks)
        blacks.pieces.append(bp4)
        bp5 = ChessPiece.PiecePawn(self, 'p5', blacks)
        blacks.pieces.append(bp5)
        bp6 = ChessPiece.PiecePawn(self, 'p6', blacks)
        blacks.pieces.append(bp6)
        bp7 = ChessPiece.PiecePawn(self, 'p7', blacks)
        blacks.pieces.append(bp7)
        bp8 = ChessPiece.PiecePawn(self, 'p8', blacks)
        blacks.pieces.append(bp8)
        br1 = ChessPiece.PieceRook(self, 'r1', blacks)
        blacks.pieces.append(br1)
        bh1 = ChessPiece.PieceHorse(self, 'h1', blacks)
        blacks.pieces.append(bh1)
        bb1 = ChessPiece.PieceBishop(self, 'b1', blacks)
        blacks.pieces.append(bb1)
        bq = ChessPiece.PieceQueen(self, 'q', blacks)
        blacks.pieces.append(bq)
        bk = ChessPiece.PieceKing(self, 'k', blacks)
        blacks.pieces.append(bk)
        bb2 = ChessPiece.PieceBishop(self, 'b2', blacks)
        blacks.pieces.append(bb2)
        bh2 = ChessPiece.PieceHorse(self, 'h2', blacks)
        blacks.pieces.append(bh2)
        br2 = ChessPiece.PieceRook(self, 'r2', blacks)
        blacks.pieces.append(br2)
        self.sides['black'] = blacks

        self.grid = {
            '8': {'a': br2, 'b': bh2, 'c': bb2, 'd': bq,  'e': bk,  'f': bb1, 'g': bh1, 'h': br1},
            '7': {'a': bp1, 'b': bp2, 'c': bp3, 'd': bp4, 'e': bp5, 'f': bp6, 'g': bp7, 'h': bp8},
            '6': {'a': '-', 'b': '-', 'c': '-', 'd': '-', 'e': '-', 'f': '-', 'g': '-', 'h': '-'},
            '5': {'a': '-', 'b': '-', 'c': '-', 'd': '-', 'e': '-', 'f': '-', 'g': '-', 'h': '-'},
            '4': {'a': '-', 'b': '-', 'c': '-', 'd': '-', 'e': '-', 'f': '-', 'g': '-', 'h': '-'},
            '3': {'a': '-', 'b': '-', 'c': '-', 'd': '-', 'e': '-', 'f': '-', 'g': '-', 'h': '-'},
            '2': {'a': wp1, 'b': wp2, 'c': wp3, 'd': wp4, 'e': wp5, 'f': wp6, 'g': wp7, 'h': wp8},
            '1': {'a': wr2, 'b': wh2, 'c': wb2, 'd': wq,  'e': wk,  'f': wb1, 'g': wh1, 'h': wr1},
        }

    def render(self):
        template = loader.get_template(self.template_name)
        context = dict()
        context['board'] = self
        context['game'] = self.game_data
        context['game_data'] = self.game_data.get_data(None)

        html_board = template.render(context)
        return html_board

    def is_cell_free(self, x, y):
        x = chr(x + 97)
        target_path = 'board/%s/%s' % (y, x)
        target_data = self.game_data.get_data(target_path)

        if target_data != '-':
            return False
        return True

    def get_piece_at(self, x, y):
        return utils.access(self.grid, '%s/%s' % (x, y))

    def target_is_friendly(self, piece, target_x, target_y):
        target_piece = self.get_piece_at(target_y, target_x)
        if target_piece != '-':
            if target_piece.side.name == piece.side.name:
                print 'you cannot kill your own pieces (%s, %s) dude ! (%s == %s)' % (target_x, target_y, target_piece.side.name, piece.side.name)
                return True
        return False

    def target_is_enemy(self, piece, target_x, target_y):
        target_piece = self.get_piece_at(target_y, target_x)
        if target_piece != "-":
            if target_piece.side.name != piece.side.name:
                print 'this is an enemy'
                return True
        return False

    def get_side_pieces(self, side):
        # print 'ChessBoard.get_side_pieces: side : %s' % side
        pieces = list()
        for line_coord, line in self.grid.items():
            for column_coord, cell in line.items():
                if cell != '-':
                    piece = cell
                    if piece.side.name == side:
                        pieces.append(piece)
        return pieces

    def get_piece_coords(self, searched_piece):
        # for line_coord, line in self.grid.items():

        for line_coord, line in self.game_data.get_data('board').items():
            # print 'ChessBoard.get_piece_coords: line_coord:%s\nline:%s' % (line_coord, line)
            for column_coord, cell in line.items():
                # print 'ChessBoard.get_piece_coords: column_coord:%s\ncell:%s' % (column_coord, cell)
                if cell != '-':
                    piece = cell
                    if cell['n'] == searched_piece.name and cell['s'] == searched_piece.side.name[0:1]:
                        return column_coord, line_coord
        print 'ChessBoard.get_piece_coords: *** warning *** piece not found : %s' % searched_piece
        return False, False

    def get_piece_from_role(self, role_name, side):
        for line_coord, line in self.grid.items():
            for column_coord, cell in line.items():
                if cell != '-':
                    piece = cell
                    if piece.role.name == role_name and piece.side.name == side:
                        # print 'ChessBoard.get_piece_from_role: piece.role.name:%s, piece.side.name:%s' \
                        #       % (piece.role.name, piece.side.name)
                        return piece
        return False

    def get_piece_coords_from_role(self, role_name, side):
        for line_coord, line in self.grid.items():
            for column_coord, cell in line.items():
                if cell != '-':
                    piece = cell
                    if piece.role.name == role_name and piece.side.name == side:
                        return column_coord, line_coord
        return False, False
