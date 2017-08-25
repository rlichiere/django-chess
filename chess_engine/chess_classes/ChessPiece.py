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

    @abstractmethod
    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        pass

    @abstractmethod
    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        # implementation must check path according to Piece capacities
        pass

    """ private """

    def _check_direction_coherence_horizontal(self, source_x, source_y, target_x, target_y):
        if source_y == target_y:
            # it's a horizontal move
            print 'PieceRook._check_direction_coherence_horizontal: True'
            return True
        print 'PieceRook._check_direction_coherence_horizontal: False'
        return False

    def _check_direction_coherence_vertical(self, source_x, source_y, target_x, target_y):
        if source_x == target_x:
            # it's a vertical move
            print 'PieceRook._check_direction_coherence_vertical: True'
            return True
        print 'PieceRook._check_direction_coherence_vertical: False'
        return False

    def _check_path_coherence_diagonal(self, source_x, source_y, target_x, target_y):
        if abs(target_x - source_x) == abs(target_y - source_y):
            return True
        return False

    def _check_path_disponibility_horizontal(self, source_x, source_y, target_x, target_y):
        if not self._check_direction_coherence_horizontal(source_x, source_y, target_x, target_y):
            print 'PieceRook._check_path_disponibility_horizontal: *** warning *** way is not coherent'
            return False

        src_x = ord(source_x) - 97
        dest_x = ord(target_x) - 97
        src_y = int(source_y)
        dest_y = int(target_y)

        path_len = abs(dest_x - src_x)
        num_step = 1
        while num_step < path_len:
            if dest_x > src_x:
                # move right
                test_x = src_x + num_step
            else:
                # move left
                test_x = src_x - num_step
            if not self.board.is_cell_free(test_x, src_y):
                print 'PieceRook._check_path_disponibility_horizontal: cell on way is not free : %s, %s' % (test_x, src_y)
                return False
            num_step += 1
        print 'PieceRook._check_path_disponibility_horizontal: True'
        return True

    def _check_path_disponibility_vertical(self, source_x, source_y, target_x, target_y):
        print 'PieceRook._check_path_disponibility_vertical (%s,%s %s,%s)' % (source_x, source_y, target_x, target_y)
        if not self._check_direction_coherence_vertical(source_x, source_y, target_x, target_y):
            print 'PieceRook._check_path_disponibility_vertical: *** warning *** way is not coherent'
            return False

        src_x = ord(source_x) - 97
        dest_x = ord(target_x) - 97
        src_y = int(source_y)
        dest_y = int(target_y)

        path_len = abs(dest_y - src_y)
        num_step = 1
        while num_step < path_len:
            if dest_y > src_y:
                # move up
                print 'PieceRook._check_path_disponibility_vertical: move up from %s,%s' % (src_x, src_y)
                test_y = src_y + num_step
            else:
                print 'PieceRook._check_path_disponibility_vertical: move down from %s, %s' % (src_x, src_y)
                # move down
                test_y = src_y - num_step
            print 'PieceRook._check_path_disponibility_vertical: test cell freedom : %s, %s' % (src_x, test_y)
            if not self.board.is_cell_free(src_x, test_y):
                print 'PieceRook._check_path_disponibility_vertical: cell on way is not free : %s, %s' % (src_x, test_y)
                return False
            num_step += 1
        print 'PieceRook._check_path_disponibility_vertical: True'
        return True

    def _check_path_disponibility_diagonal_up(self, source_x, source_y, target_x, target_y):
        pass

    def _check_path_disponibility_diagonal_down(self, source_x, source_y, target_x, target_y):
        pass

    """ utils """


class PiecePawn(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRolePawn(), 'pawn.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):

        # check if target piece is not from players color
        # target_piece = self.board.get_piece_at(dest_y, dest_x)
        # if target_piece != "-":
        #     if target_piece.side.name == self.side.name:
        #         print 'you cannot kill you pieces dude !'
        #         return False

        if self.board.target_is_friendly(self, dest_x, dest_y):
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

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        pass

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        pass


class PieceRook(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleRook(), 'rook.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):

        # check if destination is not friendly
        if self.board.target_is_friendly(self, dest_x, dest_y):
            # cannot move on a friendly piece
            return False

        # check if direction to destination is coherent with piece capacities
        if not self._check_direction_coherence(src_x, src_y, dest_x, dest_y):
            # cannot do a unattended movement
            return False
        print 'PieceRook.is_move_valid: coherence ok, let\'s see disponibility...'
        # check if path to target is disponible
        if not self._check_path_disponibility(src_x, src_y, dest_x, dest_y):
            # cannot move through another piece
            print 'PieceRook.is_move_valid: ... NO. cannot move through another piece.'
            return False

        return True

    """ abstract implementations """

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        if self._check_direction_coherence_horizontal(source_x, source_y, target_x, target_y)\
                or self._check_direction_coherence_vertical(source_x, source_y, target_x, target_y):
            print 'PieceRook._check_direction_coherence: True'
            return True
        print 'PieceRook._check_direction_coherence: False'
        return False

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        print 'PieceRook._check_path_disponibility(%s,%s %s,%s)' % (source_x, source_y, target_x, target_y)
        # check vertical
        if source_x == target_x:
            # it's a vertical move
            print 'PieceRook._check_path_disponibility: its a vertical move.'
            if self._check_path_disponibility_vertical(source_x, source_y, target_x, target_y):
                return True
            return False
        # check horizontal
        if source_y == target_y:
            # it's a horizontal move
            print 'PieceRook._check_path_disponibility: its a horizontal move.'
            if self._check_path_disponibility_horizontal(source_x, source_y, target_x, target_y):
                return True
            return False
        print 'PieceRook._check_path_disponibility: False'
        return False


class PieceHorse(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleHorse(), 'horse.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return True

    """ abstract implementations """

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        # always true for Horse
        return True

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        # always true for Horse
        return True


class PieceBishop(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleBishop(), 'bishop.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return True

    """ abstract implementations """

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        pass

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        pass


class PieceQueen(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleQueen(), 'queen.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return True

    """ abstract implementations """

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        pass

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        pass


class PieceKing(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleKing(), 'king.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return True

    """ abstract implementations """

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        pass

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        pass

