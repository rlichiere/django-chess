
from chess_engine.chess_classes import ChessBoard
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
        self.game_data.save()
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
        self.game_data.save()
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
            self.game_data.save()
            return False

        # - faire le deplacement dans la grille (dropper, popper)
        # paste piece at target position
        self.game_data.set_data('board/{line}/{column}'.format(line=y, column=x), source_piece)

        # purge source position
        self.game_data.set_data('board/{line}/{column}'.format(line=source_line, column=source_column), '-')

        # - mettre a jour le data context
        data = {
            'line': y,
            'column': x
        }
        self.game_data.set_data('token/step/data/targetCell', data)
        self.game_data.set_data('token/step/name', 'pieceMoved')
        self.game_data.save()

        # passer la main
        self._finalize_turn()

        return True

    def abandonment(self, user):
        pass

    """ end of game """
    # - accept revanche
    # - accept belle
    # - quit game (-> sauver)

    def accept_revanche(self, user):
        pass

    def accept_belle(self, user):
        pass

    def quit_game(self, user):
        pass

    """ private mechanics tools """

    def _finalize_turn(self):
        current_play_color = self.game_data.get_data('token/step/side')

        if current_play_color == 'white':
            self.game_data.set_data('token/step/side', 'black')
        else:
            self.game_data.set_data('token/step/side', 'white')

        self.game_data.set_data('token/step/name', 'waitCellSource')
        self.game_data.save()

    def _check_color_authorization(self, piece):
        # check if game accepts a move of this color
        playable_color = self.game_data.get_data('token/step/side')
        if piece.side.name != playable_color:
            print 'ChessGame._check_color_authorization: move is not valid for this color (%s, %s)' % (piece.side.name, playable_color)
            return False
        return True