import json
from json2html import *
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
        game_id = kwargs['pk']
        game_logic = ChessLogic.ChessGame(game_id)
        if game_logic:
            html_board = game_logic.board.render()
            context['html_board'] = html_board
            context['json_data'] = json2html.convert(json=game_logic.game_data.data)
            context['game_logic'] = game_logic

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

        game_logic = ChessLogic.ChessGame(game_id)
        if not game_logic:
            print ('PieceActionView.get ERROR : game not found : %s' % game_id)
            return HttpResponseRedirect(reverse('home'))

        if action == 'select':
            game_logic.move_piece_select_source(request.user, column_k, line_k)
            return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))

        elif action == 'move':
            game_logic.move_piece_select_target(request.user, column_k, line_k)
            return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))

        else:
            print 'PieceAction.get ERROR: unknown action : %s' % action
        return HttpResponseRedirect(reverse('home'))


class PiecePromoteView(View):

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs['pk']

        game_logic = ChessLogic.ChessGame(game_id)
        if not game_logic:
            print ('PieceActionView.get ERROR : game not found : %s' % game_id)
            return HttpResponseRedirect(reverse('home'))

        role_name = kwargs['role_name']
        game_logic.promote_piece(request.user, role_name)
        return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))


class MenuView(View):

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs['pk']
        game_logic = ChessLogic.ChessGame(game_id)
        if not game_logic:
            print ('PieceActionView.get ERROR : game not found : %s' % game_id)
            return HttpResponseRedirect(reverse('home'))
        action = kwargs['action']
        if action == 'abandon':
            game_logic.game_data.set_data('token/step/name', 'abandon')

            history = game_logic.game_data.get_data('history')
            history_game = dict()
            history_game['token'] = game_logic.game_data.get_data('token')
            history_game['board'] = game_logic.game_data.get_data('board')

            if history:
                new_game_key = 'game_%02d' % (len(history) + 1)
            else:
                history = dict()
                new_game_key = 'game_01'
            history[new_game_key] = history_game
            game_logic.game_data.set_data(None, {})
            game_logic.game_data.set_data('history', history)
        elif action == 'reset_game':
            history = game_logic.game_data.get_data('history')
            game_logic.game_data.set_data(None, {})
            game_logic.game_data.set_data('history', history)
        elif action == 'reset_all':
            game_logic.game_data.set_data(None, {})

        return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))
