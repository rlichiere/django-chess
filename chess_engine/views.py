import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView

from chess_classes import ChessLogic
from .models import GamePersistentData
from utils import utils


class HomeView(TemplateView):
    template_name = 'chess_engine/home.html'

    def get_context_data(self, **kwargs):
        games = GamePersistentData.objects.all()
        context = dict()
        context['games'] = games
        return {'context': context}


class GameView(TemplateView):
    template_name = 'chess_engine/game.html'

    def get_context_data(self, **kwargs):
        context = dict()
        game_data = GamePersistentData.objects.filter(id=kwargs['pk']).first()
        if game_data:
            game_logic = ChessLogic.ChessGame(game_data)
            html_board = game_logic.board.render()
            context['html_board'] = html_board
            return {'context': context}
        else:
            context['html_board'] = 'Game not found.'
            return {'context': context}


class PieceActionView(View):

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs['pk']
        action = kwargs['action']
        line_k = kwargs['line']
        column_k = kwargs['column']
        print 'PieceAction.get : game_id : %s, action : %s, line : %s, column : %s' % (game_id, action, line_k, column_k)

        game_data = GamePersistentData.objects.filter(id=game_id).first()
        if not game_data:
            print ('PieceActionView.get ERROR : game not found : %s' % game_id)
            return HttpResponseRedirect(reverse('home'))
        game_logic = ChessLogic.ChessGame(game_data)

        if action == 'select':
            # check if select source is waited :
            # current_waited_state = utils.access(game_data, 'token/step/name')
            current_waited_state = game_data.get_data('token/step/name')
            if current_waited_state != 'waitCellSource':
                print ('PieceActionView.get ERROR : do not waitCellSource : %s' % current_waited_state)
                return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))

            # save action
            data = {
                'line': line_k,
                'column': column_k
            }
            game_data.set_data('token/step/data/sourceCell', data)
            game_data.set_data('token/step/name', 'waitCellTarget')
            game_data.save()
            return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))

        elif action == 'move':
            current_waited_state = game_data.get_data('token/step/name')
            if current_waited_state != 'waitCellTarget':
                print ('PieceActionView.get ERROR : do not waitCellTarget : %s' % current_waited_state)
                return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))

            # - todo : verifier la validite du deplacement
            # copy piece from source position
            source_line = game_data.get_data('token/step/data/sourceCell/line')
            source_column = game_data.get_data('token/step/data/sourceCell/column')
            source_piece = game_logic.board.get_piece_at(source_line, source_column)
            print 'PieceActionView.get: source_piece : %s' % source_piece

            if not source_piece.is_move_valid(source_column, source_line, column_k, line_k):
                print 'PieceActionView.get: move is not valid.'
                return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))

            # - faire le deplacement dans la grille (dropper, popper)
            # paste piece at target position
            game_data.set_data('board/{line}/{column}'.format(line=line_k, column=column_k), source_piece)

            # purge source position
            game_data.set_data('board/{line}/{column}'.format(line=source_line, column=source_column), '-')

            # - mettre a jour le data context
            data = {
                'line': line_k,
                'column': column_k
            }
            game_data.set_data('token/step/data/targetCell', data)
            game_data.set_data('token/step/name', 'pieceMoved')

            # - preparer la main suivante
            # rendre le token
            game_data.set_data('token', '')
            game_data.set_data('token/step/name', 'waitCellSource')
            game_data.save()
            return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))

        else:
            print 'PieceAction.get ERROR: unknown action : %s' % action
        return HttpResponseRedirect(reverse('home'))
