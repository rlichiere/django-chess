
from chess_engine.chess_classes import ChessBoard, ChessPiece
from utils import utils
from chess_engine.models import *


class ChessGame:
    def __init__(self, game_data=None):
        self.board = ChessBoard.Board()

        if game_data:
            self.game_data = game_data
            self.load_game(game_data)
        else:
            self.game_data = self.initialize()

    def initialize(self):
        # create GamePersistentData
        # create Board
        # store board in game
        # give token to white side
        self.game_data = GamePersistentData()
        self.game_data.set_data('token/step/side', 'white')
        return self.game_data

    def load_game(self, game_id):
        # load GamePersistentData context :
        # - position of pieces on board
        # - game state (token)
        # give token to player
        self.game_data = GamePersistentData.objects.filter(id=game_id).first()
        self.board.load_grid(self.game_data)
        if not self.game_data.get_data('token/step/name'):
            self.game_data.set_data('token/step/name', 'waitCellSource')
            self.game_data.set_data('token/step/side', 'white')
        return True

    """                                    user actions """

    """ game management """
    # - start a game
    # - choose a game colorset
    # - delete a game (reserved to creator)

    def create_game(self):
        pass

    def set_game_colorset(self, color_set):
        self.board.set_color_set(color_set)

    def delete_game(self):
        pass

    """ starting game """
    # - join a game
    # - select a colorset
    # - select a side

    def join_game(self, user):
        pass

    def select_colorset(self, user, colorset):
        pass

    def select_side(self, user, side):
        pass

    """ during game """
    # - select a piece to initiate a move
    # - select a target cell to finalize a move
    # - abandon

    def move_piece_select_source(self, user, x, y):

        piece = self.board.get_piece_at(y, x)
        if not self._check_color_authorization(piece):
            return False

        # check if select source is waited :
        current_waited_state = self.game_data.get_data('token/step/name')
        if current_waited_state != 'waitCellSource':
            print ('ChessGame.move_piece_select_source ERROR : do not waitCellSource : %s' % current_waited_state)
            return False

        # save action
        data = {
            'line': y,
            'column': x
        }
        self.game_data.set_data('token/step/data', '.')
        self.game_data.set_data('token/step/data/sourceCell', data)
        self.game_data.set_data('token/step/name', 'waitCellTarget')
        return True

    def move_piece_select_target(self, user, x, y):

        # check if game accepts selection of piece
        current_waited_state = self.game_data.get_data('token/step/name')
        if current_waited_state != 'waitCellTarget':
            print ('ChessGame.move_piece_select_target : current_wait_state does not wait waitCellTarget : %s' % current_waited_state)
            return False

        # read piece from source position
        source_line = self.game_data.get_data('token/step/data/sourceCell/line')
        source_column = self.game_data.get_data('token/step/data/sourceCell/column')
        source_piece = self.board.get_piece_at(source_line, source_column)
        print 'ChessGame.move_piece_select_target: source_piece : %s' % source_piece

        if not self._check_color_authorization(source_piece):
            return False

        if not source_piece.is_move_valid(source_column, source_line, x, y):
            print 'ChessGame.move_piece_select_target: move is not valid.'
            # return to source selection
            self.game_data.set_data('token/step/data', '.')
            self.game_data.set_data('token/step/name', 'waitCellSource')
            return False

        # - faire le deplacement dans la grille (dropper, popper)

        # preparation des informations additionnelles de deplacement
        #   - si pawn move + 2 : memorize en-passant (on him on or on his trace-cell ?)
        #   todo

        target_piece = self.game_data.get_data('board/{line}/{column}'.format(line=y, column=x))

        # etablir le contexte apres deplacement :
        #   - ep case
        ep = None
        #   - rook case
        rook = None
        #   - check case
        check = None

        # positionner la piece deplacee sur la cible
        self.game_data.set_data('board/{line}/{column}'.format(line=y, column=x), source_piece)

        # memoriser le kill
        if target_piece != '-':
            print 'ChessGame.move_piece_select_target: kill memorized'
            self.game_data.set_data('token/step/data/eaten', target_piece)

        # purge source position
        self.game_data.set_data('board/{line}/{column}'.format(line=source_line, column=source_column), '-')

        # - mettre a jour le data context
        data = {
            'line': y,
            'column': x
        }
        self.game_data.set_data('token/step/data/targetCell', data)

        # check if a promotion must be purposed
        promo = self._check_promotion(source_piece, data)

        if promo:
            self.game_data.set_data('token/step/name', 'promote')
        else:
            move_data = {
                'source_piece': source_piece,
                'src_x': source_column,
                'src_y': source_line,
                'dest_x': x,
                'dest_y': y,
                'target_piece': target_piece,
                'rook': rook,
                'ep': ep,
                'check': check,
                'promo': None,
            }

            # passer la main
            self._finalize_turn(move_data)

        return True

    def promote_piece(self, user, role_name):
        # check if game accepts selection of piece
        current_waited_state = self.game_data.get_data('token/step/name')
        if current_waited_state != 'promote':
            print 'ChessGame.promote_piece : current_wait_state does not wait promote : %s' % current_waited_state
            return False

        target_line = self.game_data.get_data('token/step/data/targetCell/line')
        target_column = self.game_data.get_data('token/step/data/targetCell/column')

        side = self.game_data.get_data('token/step/side')
        target_piece_data = {
            "s": side[0:1],
            "r": role_name,
            "n": "%s_promo" % role_name
        }
        self.game_data.set_data('board/{line}/{column}'.format(line=target_line, column=target_column), target_piece_data)
        print 'ChessGame.promote_piece: Queen promoted at : %s,%s' % (target_column, target_line)

        # prepare log_data
        source_line = self.game_data.get_data('token/step/data/sourceCell/line')
        source_column = self.game_data.get_data('token/step/data/sourceCell/column')
        source_piece = self.board.get_piece_at(target_line, target_column)  # piece has still move to target
        print 'ChessGame.promote_piece: source_piece (l:%s, c:%s) : %s' % (source_line, source_column, source_piece)
        move_data = {
            'source_piece': source_piece,
            'src_x': source_column,
            'src_y': source_line,
            'target_piece': target_piece_data,
            'dest_x': target_column,
            'dest_y': target_line,
            'rook': None,
            'ep': None,     # todo
            'check': None,  # todo
            'promo': target_piece_data,  # todo
        }

        # passer la main
        self._finalize_turn(move_data)
        return True

    def abandonment(self, user):
        pass

    """ end of game """
    # - accept checkmate
    # - accept revanche
    # - accept belle
    # - quit game (-> sauver)

    def accept_checkmate(self, user):
        self.game_data.set_data('token/result', 'checkmate')

    def accept_revanche(self, user):
        pass

    def accept_belle(self, user):
        pass

    def quit_game(self, user):
        pass

    """ private mechanics tools """

    def _check_promotion(self, piece, data):
        if piece.role.name == 'P':
            if self.game_data.get_data('token/step/side') == 'white':
                promotion_line = 8
            else:
                promotion_line = 1
            if int(data['line']) == int(promotion_line):
                return True
        return False

    def _check_king_troubles_temp(self, side):
        # temporary solution to implement checkmate (done manually by player)
        # print 'ChessGame._check_king_troubles_temp: test checkmate...'
        eaten_piece = self.game_data.get_data('token/step/data/eaten')
        if eaten_piece:
            # print 'ChessGame._check_king_troubles_temp: eaten piece found : %s' % eaten_piece
            if eaten_piece['r'] == 'K':
                # the guy died, checkmate
                # print 'ChessGame._check_king_troubles_temp: check mate found.'
                return 'checkmate', []
        return False, ''

    def _check_king_troubles(self, side):
        # checks if king is in trouble.
        # - returns 'checkmate' when it's the case, and list of attacking pieces
        # - returns 'check' when it's the case, and list of attacking pieces
        # - returns False if no trouble, and empty list
        print 'GameLogic._check_kingchecks: TODO'
        king_possible_cells = list()    # liste du roi (= la ou il peut se deplacer sans etre attaque)
        king_forbidden_cells = list()   # liste des interdits du roi
        target_cells = list()           # liste de cellules cibles
        attackingPieces = dict()        # dictionnaire des attaquants

        # find king in board

        # memoriser la position du roi
        # construire la liste des deplacements possibles du roi

        # parcourir la liste des pieces opposees au roi
        #   pour chaque piece:
        #       construire la liste des cellules que la piece attaque
        #       pour chaque cellule que la piece attaque:
        #           si la cellule est dans la liste du roi:
        #               ajouter la piece dans la liste des attaquants (si elle n'y est pas deja)
        #               ajouter la cellule dans la liste d'interdits du roi (si elle n'y est pas deja)
        king_forbidden_cells.append('e7')
        king_possible_cells.append('e7')
        # si le roi est attaque:
        if len(king_forbidden_cells) > 0:
            if len(king_possible_cells) == len(king_forbidden_cells):
                # le roi ne peut pas bouger
                result = 'check'    # 'checkmate'
            else:
                result = 'check'
            # sauver la liste des attaquants
            self.game_data.set_data('token/step/attackers', attackingPieces)
            return result, attackingPieces
        else:
            self.game_data.set_data('token/step/attackers', {})
        return False, []

    def _finalize_turn(self, move_data):

        # - king-checks
        side = self.game_data.get_data('token/step/side')

        # ecrire le log
        self.game_data.add_log(move_data)

        king_checks = self._check_king_troubles_temp(side)                           # todo : remake properly
        # print ('ChessGame._finalize_turn: king_checks : %s' % king_checks.__str__())
        # if king_checks[0] == 'checkmate':

        if king_checks[0] == 'checkmate':
            self.game_data.set_data('token/step/name', 'checkmate')
            print 'ChessGame._finalize_turn: checkmate set.'
        else:
            # no trouble or simple check
            self.game_data.set_data('token/step/name', 'waitCellSource')
        if side == 'white':
            self.game_data.set_data('token/step/side', 'black')
        else:
            self.game_data.set_data('token/step/side', 'white')

    def _check_color_authorization(self, piece):
        # check if game accepts a move of this color
        playable_color = self.game_data.get_data('token/step/side')
        if piece.side.name != playable_color:
            print 'ChessGame._check_color_authorization: move is not valid for this color (%s, %s)' % (piece.side.name, playable_color)
            return False
        return True
