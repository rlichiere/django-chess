from abc import ABCMeta, abstractmethod


class PieceRole:
    def __init__(self, name, label, weight):
        self.name = name
        self.label = label
        self.weight = weight


class PieceRolePawn(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'P', 'Pawn', 1)


class PieceRoleRook(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'R', 'Rook', 5)


class PieceRoleHorse(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'H', 'Horse', 3)


class PieceRoleBishop(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'B', 'Bishop', 3)


class PieceRoleQueen(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'Q', 'Queen', 9)


class PieceRoleKing(PieceRole):
    def __init__(self):
        PieceRole.__init__(self, 'K', 'King', 0)


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

    """ public """

    def is_in_danger(self, src_c, src_l):
        # print 'Piece.is_in_danger(src_c:%s, src_l:%s) begins.' % (src_c, src_l)
        ennemy_side = 'black' if self.side.name == 'white' else 'white'
        ennemy_pieces = self.board.get_side_pieces(ennemy_side)
        # print 'Piece.is_in_danger: ennemy_side:%s' % ennemy_side
        for ennemy_piece in ennemy_pieces:
            # print 'Piece.is_in_danger: ennemy_piece:%s' % ennemy_piece
            ennemy_piece_c, ennemy_piece_l = self.board.get_piece_coords(ennemy_piece)
            if ennemy_piece_c and ennemy_piece_l:
                # print 'Piece.is_in_danger: ennemy %s (c:%s, l:%s)' % (ennemy_piece, ennemy_piece_c, ennemy_piece_l)
                if ennemy_piece.is_move_valid(ennemy_piece_c, ennemy_piece_l, src_c, src_l):
                    print 'Piece.is_in_danger: %s is targeted by %s' % (self, ennemy_piece)
                    return True
        # print 'Piece.is_in_danger(src_c:%s, src_l:%s) False.' % (src_c, src_l)
        return False

    """ private """

    def _is_move_valid_generic(self, src_x, src_y, dest_x, dest_y):
        if self.board.target_is_friendly(self, dest_x, dest_y):
            return False
        if not self._check_direction_coherence(src_x, src_y, dest_x, dest_y):
            # print 'Piece._is_move_valid_generic: direction incoherent'
            return False
        if not self._check_path_disponibility(src_x, src_y, dest_x, dest_y):
            # print 'Piece._is_move_valid_generic: path indisponible'
            return False
        return True

    def _check_direction_coherence_horizontal(self, source_x, source_y, target_x, target_y):
        if source_y == target_y:
            # it's a horizontal move
            return True
        return False

    def _check_direction_coherence_vertical(self, source_x, source_y, target_x, target_y):
        if source_x == target_x:
            # it's a vertical move
            return True
        return False

    def _check_path_coherence_diagonal(self, source_x, source_y, target_x, target_y):

        src_x = ord(source_x) - 97
        dest_x = ord(target_x) - 97
        src_y = int(source_y)
        dest_y = int(target_y)
        if abs(dest_x - src_x) == abs(dest_y - src_y):
            return True
        return False

    def _check_path_disponibility_horizontal(self, source_x, source_y, target_x, target_y):
        if not self._check_direction_coherence_horizontal(source_x, source_y, target_x, target_y):
            # print 'Piece._check_path_disponibility_horizontal: *** warning *** way is not coherent'
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
                # print 'Piece._check_path_disponibility_horizontal: cell on way is not free : %s, %s' % (test_x, src_y)
                return False
            num_step += 1
        return True

    def _check_path_disponibility_vertical(self, source_x, source_y, target_x, target_y):
        if not self._check_direction_coherence_vertical(source_x, source_y, target_x, target_y):
            # print 'Piece._check_path_disponibility_vertical: *** warning *** way is not coherent'
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
                test_y = src_y + num_step
            else:
                # move down
                test_y = src_y - num_step
            if not self.board.is_cell_free(src_x, test_y):
                return False
            num_step += 1
        return True

    def _check_path_disponibility_diagonal(self, source_x, source_y, target_x, target_y):

        if not self._check_path_coherence_diagonal(source_x, source_y, target_x, target_y):
            return False

        src_x = ord(source_x) - 97
        dest_x = ord(target_x) - 97
        src_y = int(source_y)
        dest_y = int(target_y)

        path_len = abs(dest_x - src_x)
        if dest_x > src_x and dest_y > src_y:
            # go top right
            num_step = 1
            while num_step < path_len:
                if not self.board.is_cell_free(src_x + num_step, src_y + num_step):
                    return False
                num_step += 1
            return True
        elif dest_x > src_x and dest_y < src_y:
            # go down right
            num_step = 1
            while num_step < path_len:
                if not self.board.is_cell_free(src_x + num_step, src_y - num_step):
                    return False
                num_step += 1
            return True
        elif dest_x < src_x and dest_y < src_y:
            # go down left
            num_step = 1
            while num_step < path_len:
                if not self.board.is_cell_free(src_x - num_step, src_y - num_step):
                    return False
                num_step += 1
            return True
        elif dest_x < src_x and dest_y > src_y:
            # go top left
            num_step = 1
            while num_step < path_len:
                if not self.board.is_cell_free(src_x - num_step, src_y + num_step):
                    return False
                num_step += 1
            return True
        else:
            print 'Piece._check_path_disponibility_vertical: strange case'
            return False

    """ utils """


class PiecePawn(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRolePawn(), 'pawn.png', side)

    """ abstract implementations """

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return self._is_move_valid_specific(src_x, src_y, dest_x, dest_y)

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        pass

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        # always true for Pawn
        return True

    """ private specific implementations """

    def _is_move_valid_specific(self, src_x, src_y, dest_x, dest_y):
        # print 'PiecePawn.is_move_valid: begins'

        if self.board.target_is_friendly(self, dest_x, dest_y):
            return False

        src_x = ord(src_x) - 97
        dest_x = ord(dest_x) - 97
        src_y = int(src_y)
        dest_y = int(dest_y)

        if self.side.name == 'white':
            start_axis = 2
        else:
            start_axis = 7

        enpassant_data = self.board.game_data.get_data('token/step/enpassant')
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
                    print 'PiecePawn.is_move_valid: wrong way'
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
                    print 'PiecePawn.is_move_valid: wrong way'
                    return False

                if src_y - dest_y <= max_len:
                    # si dest_x,dest_y est occupee, on ne peut pas s'y deplacer
                    if not self.board.is_cell_free(dest_x, dest_y):
                        print 'PiecePawn.is_move_valid: target is not free'
                        return False
                    return True

        elif (abs(dest_x - src_x) == 1) and (abs(dest_y - src_y) == 1):
            # attack move

            # special cases
            # check enpassant case
            if enpassant_data:
                if (dest_y == enpassant_data['y']) and (dest_x == enpassant_data['x']):
                    print 'PiecePawn._is_move_valid_specific: enpassable :D'
                    return True
                else:
                    # print 'PiecePawn._is_move_valid_specific: no enpassable :('
                    pass

            # normal cases
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

        # print 'default False'
        return False


class PieceRook(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleRook(), 'rook.png', side)

    """ abstract implementations """

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return self._is_move_valid_generic(src_x, src_y, dest_x, dest_y)

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        if self._check_direction_coherence_horizontal(source_x, source_y, target_x, target_y)\
                or self._check_direction_coherence_vertical(source_x, source_y, target_x, target_y):
            return True
        return False

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        if self._check_path_disponibility_vertical(source_x, source_y, target_x, target_y):
            return True
        if self._check_path_disponibility_horizontal(source_x, source_y, target_x, target_y):
            return True
        return False


class PieceHorse(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleHorse(), 'horse.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return self._is_move_valid_generic(src_x, src_y, dest_x, dest_y)

    """ abstract implementations """

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        src_x = ord(source_x) - 97
        dest_x = ord(target_x) - 97
        src_y = int(source_y)
        dest_y = int(target_y)

        # list targetable cells

        targetable = list()
        cell_1_h_x = src_x + 1
        cell_1_h_y = src_y + 2
        # if not cell_1_h_x > 7:
        #     if not cell_1_h_y > 8:
        targetable.append({'x': cell_1_h_x, 'y': cell_1_h_y, 'name': '1h'})

        cell_2_h_x = src_x + 2
        cell_2_h_y = src_y + 1
        # if not cell_2_h_x > 7:
        #     if not cell_2_h_y > 8:
        targetable.append({'x': cell_2_h_x, 'y': cell_2_h_y, 'name': '2h'})

        cell_4_h_x = src_x + 2
        cell_4_h_y = src_y - 1
        # if not cell_4_h_x > 7:
        #     if not cell_4_h_y < 1:
        targetable.append({'x': cell_4_h_x, 'y': cell_4_h_y, 'name': '4h'})

        cell_5_h_x = src_x + 1
        cell_5_h_y = src_y - 2
        # if not cell_5_h_x > 7:
        #     if not cell_5_h_y < 1:
        targetable.append({'x': cell_5_h_x, 'y': cell_5_h_y, 'name': '5h'})

        cell_7_h_x = src_x - 1
        cell_7_h_y = src_y - 2
        # if not cell_7_h_x < 1:
        #     if not cell_7_h_y < 0:
        targetable.append({'x': cell_7_h_x, 'y': cell_7_h_y, 'name': '7h'})

        cell_8_h_x = src_x - 2
        cell_8_h_y = src_y - 1
        # if not cell_8_h_x < 1:
        #     if not cell_8_h_y < 0:
        targetable.append({'x': cell_8_h_x, 'y': cell_8_h_y, 'name': '8h'})

        cell_10_h_x = src_x - 2
        cell_10_h_y = src_y + 1
        # if not cell_10_h_x < 1:
        #     if not cell_10_h_y > 8:
        targetable.append({'x': cell_10_h_x, 'y': cell_10_h_y, 'name': '10h'})

        cell_11_h_x = src_x - 1
        cell_11_h_y = src_y + 2
        # if not cell_11_h_x < 1:
        #     if not cell_11_h_y > 8:
        targetable.append({'x': cell_11_h_x, 'y': cell_11_h_y, 'name': '11h'})

        # check if target is in targetable list
        for cell in targetable:
            if cell['x'] == dest_x and cell['y'] == dest_y:
                return True
        return False

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        # always true for Horse
        return True


class PieceBishop(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleBishop(), 'bishop.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return self._is_move_valid_generic(src_x, src_y, dest_x, dest_y)

    """ abstract implementations """

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        if self._check_path_coherence_diagonal(source_x, source_y, target_x, target_y):
            return True
        return False

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        if self._check_path_disponibility_diagonal(source_x, source_y, target_x, target_y):
            return True
        return False


class PieceQueen(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleQueen(), 'queen.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        return self._is_move_valid_generic(src_x, src_y, dest_x, dest_y)

    """ abstract implementations """

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        if self._check_direction_coherence_horizontal(source_x, source_y, target_x, target_y)\
                or self._check_direction_coherence_vertical(source_x, source_y, target_x, target_y):
            return True
        if self._check_path_coherence_diagonal(source_x, source_y, target_x, target_y):
            return True
        return False

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        if self._check_path_disponibility_vertical(source_x, source_y, target_x, target_y):
            return True
        if self._check_path_disponibility_horizontal(source_x, source_y, target_x, target_y):
            return True
        if self._check_path_disponibility_diagonal(source_x, source_y, target_x, target_y):
            return True
        return False


class PieceKing(Piece):
    def __init__(self, board, name, side):
        Piece.__init__(self, board, name, PieceRoleKing(), 'king.png', side)

    def is_move_valid(self, src_x, src_y, dest_x, dest_y):
        # check castle case
        castle_call_case = self.detect_castle_call(src_x, src_y, dest_x, dest_y)
        if castle_call_case:
            # king must not be checked
            if self.is_in_danger(src_x, src_y):
                return False
            rookables = self.board.game_data.get_data('token/step/castle/%s' % self.side.name)
            if castle_call_case in rookables:
                # check path disponibility
                if self._check_path_disponibility_horizontal(src_x, src_y, dest_x, dest_y):
                    if self.board.get_piece_at(dest_y, dest_x) != '-':
                        # target cell must be free
                        return False

                    # check if path is not checked
                    if self._castle_path_is_targeted(castle_call_case):
                        return False
                    print 'PieceKing.is_move_valid: castle call valid on %s' % castle_call_case
                    return True
            return False
        # normal case
        return self._is_move_valid_generic(src_x, src_y, dest_x, dest_y)

    def detect_castle_call(self, source_x, source_y, target_x, target_y):
        src_x = ord(source_x) - 97
        dest_x = ord(target_x) - 97
        src_y = int(source_y)
        dest_y = int(target_y)
        if self.side.name == 'white' and src_y == 1 or self.side.name == 'black' and src_y == 8:
            if dest_y == src_y:
                # vertical rule ok
                if dest_x - src_x == 2:
                    # horizontal rule points r1
                    return 'r1'
                elif src_x - dest_x == 2:
                    # horizontal rule points r2
                    return 'r2'
        return False

    def move_rook(self, game_data, rook_name):
        rook_x = 'h' if rook_name == 'r1' else 'a'
        rook_y = 1 if self.side.name == 'white' else 8
        target_x = 'f' if rook_name == 'r1' else 'd'
        target_y = 1 if self.side.name == 'white' else 8
        rook_piece = self.board.get_piece_at(rook_y, rook_x)
        game_data.set_data('board/{line}/{column}'.format(line=rook_y, column=rook_x), '-')
        game_data.set_data('board/{line}/{column}'.format(line=target_y, column=target_x), rook_piece)

    """ abstract implementations """

    def _check_direction_coherence(self, source_x, source_y, target_x, target_y):
        src_x = ord(source_x) - 97
        dest_x = ord(target_x) - 97
        src_y = int(source_y)
        dest_y = int(target_y)
        if self._check_direction_coherence_horizontal(source_x, source_y, target_x, target_y) and abs(dest_x - src_x) == 1:
            return True
        if self._check_direction_coherence_vertical(source_x, source_y, target_x, target_y) and abs(dest_y - src_y) == 1:
            return True
        if self._check_path_coherence_diagonal(source_x, source_y, target_x, target_y) and abs(dest_x - src_x) == 1:
            return True
        return False

    def _check_path_disponibility(self, source_x, source_y, target_x, target_y):
        # always True for King
        return True

    """ private tools """

    def _castle_path_is_targeted(self, castle_call_case):
        target_x = 'f' if castle_call_case == 'r1' else 'd'
        target_y = 1 if self.side.name == 'white' else 8
        if self.is_in_danger(target_x, target_y):
            return True
        return False
