from abc import ABCMeta, abstractmethod

class PieceRole:
    def __init__(self, name, label):
        self.name = name
        self.label = label


class PieceRolePawn(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'P', 'Pawn')


class PieceRoleRook(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'R', 'Rook')


class PieceRoleHorse(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'H', 'Horse')


class PieceRoleBishop(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'B', 'Bishop')


class PieceRoleQueen(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'Q', 'Queen')


class PieceRoleKing(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'K', 'King')


class Piece(object):
    __metaclass__ = ABCMeta

    def __init__(self, board, name, role, picture, side):
        self.name = name
        self.role = role
        self.side = side
        self.picture = picture

        self.board = board

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __json__(self):
        return {'n': self.name, 'r': self.role.name, 's': self.side.name[0:1]}

    """ abstract public """

    @abstractmethod
    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        # check if move is valid according to piece role and grid content
        return True

    """ abstract private """


class PiecePawn(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRolePawn(), 'pawn.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):

        # check if target piece is not from players color
        target_piece = self.board.get_piece_at(dest_y, dest_x)
        if target_piece != "-":
            if target_piece.side.name == self.side.name:
                print 'you cannot kill you pieces dude !'
                return False

        src_x = ord(src_x) - 97
        dest_x = ord(dest_x) - 97
        src_y = int(src_y)
        dest_y = int(dest_y)
        print 'PiecePawn.is_move_valid: src_x:%s, src_y:%s, dest_x:%s, dest_y:%s' % (src_x, src_y, dest_x, dest_y)

        if self.side.name == 'white':
            start_axis = 2
        else:
            start_axis = 7

        if src_x == dest_x:
            # move front side
            if src_y == start_axis:
                # can move of 1 or 2 cases front
                max_len = 2
            else:
                # can move of 1 case front
                max_len = 1
            if self.side.name == 'white':
                # check if move in good way
                if not dest_y > src_y:
                    return False

                if dest_y - src_y <= max_len:
                    # si dest_x,dest_y est occupee, on ne peut pas s'y deplacer
                    if not self.board.is_cell_free(dest_x, dest_y):
                        print 'PiecePawn.is_move_valid: target is not free'
                        return False
                    return True
            else:
                # check if move in good way
                if not dest_y < src_y:
                    return False

                if src_y - dest_y <= max_len:
                    # si dest_x,dest_y est occupee, on ne peut pas s'y deplacer
                    if not self.board.is_cell_free(dest_x, dest_y):
                        return False
                    return True

        elif (abs(dest_x - src_x) == 1) and (abs(dest_y - src_y) == 1):
            # attack move

            # check if move in good way
            if self.side.name == 'white':
                if not dest_y > src_y:
                    return False
            else:
                if not dest_y < src_y:
                    return False

            if self.board.is_cell_free(dest_x, dest_y):
                return False
            return True

        return False


class PieceRook(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleRook(), 'rook.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return True


class PieceHorse(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleHorse(), 'horse.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return True


class PieceBishop(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleBishop(), 'bishop.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return True


class PieceQueen(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleQueen(), 'queen.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return True


class PieceKing(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleKing(), 'king.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return True


