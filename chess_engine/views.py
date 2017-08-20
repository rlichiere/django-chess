import json
from django.http import HttpResponse
from django.views.generic import View, TemplateView

from chess_classes import ChessLogic
from .models import GamePersistentData


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
        game_data = GamePersistentData.objects.filter(id=kwargs['id']).first()
        if game_data:
            game_logic = ChessLogic.ChessGame(game_data)
            html_board = game_logic.board.render()
            context['html_board'] = html_board
            return {'context': context}
        else:
            context['html_board'] = 'Game not found.'
            return {'context': context}


class PieceActionView(View):

    def get(self, **kwargs):
        action = kwargs['action']
        line_k = kwargs['line']
        column_k = kwargs['column']
        print 'PieceAction.get : action : %s, line : %s, column : %s' % (action, line_k, column_k)
        result = dict()
        if kwargs['action'] == 'select':
            pass
        elif kwargs['action'] == 'move':
            pass
        else:
            print 'PieceAction.get ERROR: unknown action : %s' % action

        return HttpResponse(json.dumps(result))
