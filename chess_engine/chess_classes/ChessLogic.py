
from chess_engine.chess_classes import ChessBoard, ChessPiece
from utils import utils
from chess_engine.models import *


class ChessGame:
    def __init__(self, game_id=None):
        self.board = ChessBoard.Board()

        if game_id:
            self.game_id = game_id
            self.load_game(game_id)
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
        self.game_id = game_id
        self.game_data = GamePersistentData.objects.filter(id=self.game_id).first()
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

        # prepare own king check verifications
        backup_before_move = self._backup_context_data_before_move()

        if not source_piece.is_move_valid(source_column, source_line, x, y):
            print 'ChessGame.move_piece_select_target: move is not valid.'
            # return to source selection
            self.game_data.set_data('token/step/data', '.')
            self.game_data.set_data('token/step/name', 'waitCellSource')
            return False

        # prepare owncheck analyze :
        # save board
        # play move
        # check own king troubles
        # if troubles found,
        #   restore backuped board
        # else
        #   continue

        # - faire le deplacement dans la grille (dropper, popper)

        # preparation des informations additionnelles de deplacement
        #   - si pawn move + 2 : memorize en-passant (on him on or on his trace-cell ?)
        enpassant_set = None
        if source_piece.role.name == 'P':
            enpassant_set = self._prepare_enpassant_vulnerability(source_column, source_line, source_piece, x, y)
            if enpassant_set:
                # print 'ChessGame.move_piece_select_target: enpassant vulnerability set.'
                pass

        target_piece = self.game_data.get_data('board/{line}/{column}'.format(line=y, column=x))

        # etablir le contexte apres deplacement :
        #   - ep case
        ep = False
        enpassed_piece = None
        enpassant_data = self.game_data.get_data('token/step/enpassant')
        if source_piece.role.name == 'P' and enpassant_data:
            src_x = ord(x) - 97
            src_y = int(y)
            if (src_x == enpassant_data['x']) and (src_y == enpassant_data['y']):
                ep = True
                enpassed_x = x
                if source_piece.side.name == 'white':
                    enpassed_y = str(int(y)-1)
                else:
                    enpassed_y = str(int(y) + 1)
                print 'ChessGame.move_piece_select_target: En passant done for y:%s, x:%s.' % (y, x)
                enpassed_piece = self.game_data.get_data('board/{line}/{column}'.format(line=enpassed_y, column=enpassed_x))
                self.game_data.set_data('token/step/data/eaten', enpassed_piece)
                self.game_data.set_data('board/{line}/{column}'.format(line=enpassed_y, column=x), '-')

        #   - rook case
        rook = None

        # positionner la piece deplacee sur la cible
        self.game_data.set_data('board/{line}/{column}'.format(line=y, column=x), source_piece)

        # memoriser le kill
        if target_piece != '-':
            print 'ChessGame.move_piece_select_target: kill memorized'
            self.game_data.set_data('token/step/data/eaten', target_piece)

        # purge source position
        self.game_data.set_data('board/{line}/{column}'.format(line=source_line, column=source_column), '-')

        # purge enpassant vulnerability
        if not enpassant_set:
            self.board.game_data.pop_data('token/step', 'enpassant')
            # print 'ChessGame.move_piece_select_target: enpassant popped'

        # - mettre a jour le data context et la grid
        data = {
            'line': y,
            'column': x
        }
        self.game_data.set_data('token/step/data/targetCell', data)
        self.board.set_piece_at(y, x, source_piece)

        # # move is done
        # we can now check if own king is checked (then reload backuped data)
        if self._is_kingchecked(source_piece.side.name):
            print 'ChessGame.move_piece_select_target: own king is checked.'
            self._restore_context_data_from_backup(backup_before_move)
            self.game_data.set_data('token/step/data/impossible_move', 'king_checked')
            return False
        self.game_data.set_data('token/step/data/impossible_move', '')

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
                'promo': None,                  # impossible to promo outside promote_piece case
                'check': None,  # will be set in _finalize
            }
            if ep:
                move_data['target_piece'] = enpassed_piece
            else:
                move_data['target_piece'] = target_piece

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
        # print 'ChessGame.promote_piece: source_piece (l:%s, c:%s) : %s' % (source_line, source_column, source_piece)
        move_data = {
            'source_piece': source_piece,
            'src_x': source_column,
            'src_y': source_line,
            'target_piece': target_piece_data,
            'dest_x': target_column,
            'dest_y': target_line,
            'promo': target_piece_data,
            'rook': None,                   # impossible to promote with rook
            'ep': None,                     # impossible to promote with enpassant
            'check': None,                  # will be set in _finalize
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

    def _backup_context_data_before_move(self):
        backup = dict()
        backup['obj_board'] = self.board
        backup['obj_game_data'] = self.game_data
        backup['sql_game_data'] = self.game_data.get_data('')
        return backup

    def _is_kingchecked(self, side_name):
        king = self.board.get_piece_from_role('K', side_name)
        king_c, king_l = self.board.get_piece_coords(king)

        if king.is_in_danger(king_c, king_l):
                return True
        return False

    def _restore_context_data_from_backup(self, backup):
        self.board = backup['obj_board']
        self.game_data = backup['obj_game_data']
        self.game_data.set_data('', backup['sql_game_data'])

    def _prepare_enpassant_vulnerability(self, source_x, source_y, source_piece, target_x, target_y):
        src_x = ord(source_x) - 97
        dest_x = ord(target_x) - 97
        src_y = int(source_y)
        dest_y = int(target_y)
        if source_piece.side.name == 'white':
            start_axis = 2
            enpassant_cell = {'x': dest_x, 'y': int(dest_y) - 1}
        else:
            start_axis = 7
            enpassant_cell = {'x': dest_x, 'y': int(dest_y) + 1}

        if src_y != start_axis:
            return False

        if abs(dest_y - src_y) == 2:
            # memorize enpassant
            # print 'ChessGame._prepare_enpassant_vulnerability: enpassant set.'
            self.game_data.set_data('token/step/enpassant', enpassant_cell)
            return enpassant_cell
        return False

    def _if_eaten_piece_was(self, piece_role):
        eaten_piece = self.game_data.get_data('token/step/data/eaten')
        if eaten_piece:
            if eaten_piece['r'] == piece_role:
                return True
        return False

    def _check_king_troubles(self, side_name):
        # temporary easy solution to detect checkmate (works only after a complete move)
        if self._if_eaten_piece_was('K'):
            return True, 'checkmate'

        # find king in board
        king = self.board.get_piece_from_role('K', side_name)
        if not king:
            print 'No %s king found !' % side_name
            return False, None
        king_c, king_l = self.board.get_piece_coords_from_role('K', side_name)
        print 'ChessGame._check_king_troubles: king found : %s (x:%s, y:%s)' % (king, king_c, king_l)
        if king.is_in_danger(king_c, king_l):
            # print 'ChessGame._check_king_troubles: king is in danger. True.'
            return True, 'check'
        # print 'ChessGame._check_king_troubles: False.'
        return False, None

    def _finalize_turn(self, move_data):
        # - king-checks
        side = self.game_data.get_data('token/step/side')

        # reload grid
        self.board.load_grid(self.game_data)

        ennemy_side = 'black' if side == 'white' else 'white'
        king_checks = self._check_king_troubles(ennemy_side)
        # print ('ChessGame._finalize_turn: king_checks : %s' % king_checks.__str__())

        if king_checks[1] == 'checkmate':
            move_data['check'] = 'checkmate'
            self.game_data.set_data('token/step/name', 'checkmate')
            print 'ChessGame._finalize_turn: checkmate set.'
        else:
            # no trouble or simple check
            if king_checks[1] == 'check':
                move_data['check'] = 'check'
            self.game_data.set_data('token/step/name', 'waitCellSource')

        # ecrire le log
        self.game_data.add_log(move_data)

        if side == 'white':
            self.game_data.set_data('token/step/side', 'black')
        else:
            self.game_data.set_data('token/step/side', 'white')
        print 'TURN FINALIZED'

    def _check_color_authorization(self, piece):
        # check if game accepts a move of this color
        playable_color = self.game_data.get_data('token/step/side')
        if piece.side.name != playable_color:
            print 'ChessGame._check_color_authorization: move is not valid for this color (%s, %s)' % (piece.side.name, playable_color)
            return False
        return True
