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


class Board:
    template_name = 'chess_engine/board.html'

    def __init__(self, color_set):
        print 'ChessBoard.__init__'
        self.color_set = color_set
        self.grid = dict()
        self.game_data = None
        self.sides = dict()
        self.sides['white'] = Side('white')
        self.sides['black'] = Side('black')

    def load_grid(self, game_data):
        self.game_data = game_data
        loaded_grid = game_data.get_data(None)
        if len(loaded_grid) < 8:
            self.load_new_grid()
            self.game_data.set_data(None, self.grid)
            self.game_data.save()
            print 'Board.load_grid: unfound data, so created some.'
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
                            piece = ChessPiece.PiecePawn(cell['n'], side)
                        elif cell['r'] == 'R':
                            piece = ChessPiece.PieceRook(cell['n'], side)
                        elif cell['r'] == 'H':
                            piece = ChessPiece.PieceHorse(cell['n'], side)
                        elif cell['r'] == 'B':
                            piece = ChessPiece.PieceBishop(cell['n'], side)
                        elif cell['r'] == 'Q':
                            piece = ChessPiece.PieceQueen(cell['n'], side)
                        elif cell['r'] == 'K':
                            piece = ChessPiece.PieceKing(cell['n'], side)
                        utils.access(self.grid, '%s/%s' % (line_key, cell_key), piece)
                        # self.grid[line_key][cell_key] = piece
        print 'Board.load_grid: loaded.'

    def save_grid(self):
        self.game_data.set_data('', self.grid)
        print 'Board.load_grid: loaded.'

    def load_new_grid(self):
        whites = Side('white')
        wp1 = ChessPiece.PiecePawn('p1', whites)
        whites.pieces.append(wp1)
        wp2 = ChessPiece.PiecePawn('p2', whites)
        whites.pieces.append(wp2)
        wp3 = ChessPiece.PiecePawn('p3', whites)
        whites.pieces.append(wp3)
        wp4 = ChessPiece.PiecePawn('p4', whites)
        whites.pieces.append(wp4)
        wp5 = ChessPiece.PiecePawn('p5', whites)
        whites.pieces.append(wp5)
        wp6 = ChessPiece.PiecePawn('p6', whites)
        whites.pieces.append(wp6)
        wp7 = ChessPiece.PiecePawn('p7', whites)
        whites.pieces.append(wp7)
        wp8 = ChessPiece.PiecePawn('p8', whites)
        whites.pieces.append(wp8)
        wr1 = ChessPiece.PieceRook('r1', whites)
        whites.pieces.append(wr1)
        wh1 = ChessPiece.PieceHorse('h1', whites)
        whites.pieces.append(wh1)
        wb1 = ChessPiece.PieceBishop('b1', whites)
        whites.pieces.append(wb1)
        wq = ChessPiece.PieceQueen('q', whites)
        whites.pieces.append(wq)
        wk = ChessPiece.PieceKing('k', whites)
        whites.pieces.append(wk)
        wb2 = ChessPiece.PieceBishop('b2', whites)
        whites.pieces.append(wb2)
        wh2 = ChessPiece.PieceHorse('h2', whites)
        whites.pieces.append(wh2)
        wr2 = ChessPiece.PieceRook('r2', whites)
        whites.pieces.append(wr2)
        self.sides['white'] = whites

        blacks = Side('black')
        bp1 = ChessPiece.PiecePawn('p1', blacks)
        blacks.pieces.append(bp1)
        bp2 = ChessPiece.PiecePawn('p2', blacks)
        blacks.pieces.append(bp2)
        bp3 = ChessPiece.PiecePawn('p3', blacks)
        blacks.pieces.append(bp3)
        bp4 = ChessPiece.PiecePawn('p4', blacks)
        blacks.pieces.append(bp4)
        bp5 = ChessPiece.PiecePawn('p5', blacks)
        blacks.pieces.append(bp5)
        bp6 = ChessPiece.PiecePawn('p6', blacks)
        blacks.pieces.append(bp6)
        bp7 = ChessPiece.PiecePawn('p7', blacks)
        blacks.pieces.append(bp7)
        bp8 = ChessPiece.PiecePawn('p8', blacks)
        blacks.pieces.append(bp8)
        br1 = ChessPiece.PieceRook('r1', blacks)
        blacks.pieces.append(br1)
        bh1 = ChessPiece.PieceHorse('h1', blacks)
        blacks.pieces.append(bh1)
        bb1 = ChessPiece.PieceBishop('b1', blacks)
        blacks.pieces.append(bb1)
        bq = ChessPiece.PieceQueen('q', blacks)
        blacks.pieces.append(bq)
        bk = ChessPiece.PieceKing('k', blacks)
        blacks.pieces.append(bk)
        bb2 = ChessPiece.PieceBishop('b2', blacks)
        blacks.pieces.append(bb2)
        bh2 = ChessPiece.PieceHorse('h2', blacks)
        blacks.pieces.append(bh2)
        br2 = ChessPiece.PieceRook('r2', blacks)
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
        context['grid'] = self.grid
        html_board = template.render(context)
        return html_board
