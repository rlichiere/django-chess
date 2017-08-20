
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
    def __init__(self, name, role, picture, side):
        self.name = name
        self.role = role
        self.side = side
        self.picture = picture

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __json__(self):
        return {'n': self.name, 'r': self.role.name, 's': self.side.name[0:1]}


class PiecePawn(Piece):
    def __init__(self, name, side):
        Piece.__init__(self, name, PieceRolePawn(), 'pawn.png', side)


class PieceRook(Piece):
    def __init__(self, name, side):
        Piece.__init__(self, name, PieceRoleRook(), 'rook.png', side)


class PieceHorse(Piece):
    def __init__(self, name, side):
        Piece.__init__(self, name, PieceRoleHorse(), 'horse.png', side)


class PieceBishop(Piece):
    def __init__(self, name, side):
        Piece.__init__(self, name, PieceRoleBishop(), 'bishop.png', side)


class PieceQueen(Piece):
    def __init__(self, name, side):
        Piece.__init__(self, name, PieceRoleQueen(), 'queen.png', side)


class PieceKing(Piece):
    def __init__(self, name, side):
        Piece.__init__(self, name, PieceRoleKing(), 'king.png', side)
