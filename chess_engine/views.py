from json2html import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView, FormView

from chess_classes import ChessLogic
from .forms import *


class HomeView(TemplateView):
    template_name = 'chess_engine/home.html'

    def get_context_data(self, *args, **kwargs):
        games = GamePersistentData.objects.all()
        context = super(HomeView, self).get_context_data(**kwargs)

        opened_games = list()
        running_games = list()
        finished_games = list()
        for game in games:
            white_user_id = game.get_data('participants/white/1')
            black_user_id = game.get_data('participants/black/1')
            if not white_user_id or not black_user_id:
                opened_games.append(game)
                continue

            step = game.get_data('token/step/name')
            print 'game_id : %s, step_name : %s' % (game.id, step)
            if not step:
                finished_games.append(game)
                print 'added to finished games (len:%s)' % len(finished_games)
                continue

            rounds = game.get_data('rounds')
            if not rounds:
                running_games.append(game)
                print 'added to running games (len:%s)' % len(running_games)
                continue

            white_wins = 0
            black_wins = 0
            for round_k, round in rounds.items():
                if round['winner'] == 'white':
                    white_wins += 1
                elif round['winner'] == 'black':
                    black_wins += 1
            winning_games = int(game.get_data('game_options/winning_games'))
            if white_wins >= winning_games or black_wins >= winning_games:
                print 'added to finished games2 (len:%s)' % len(finished_games)
                finished_games.append(game)
                continue

            print 'added to running games2 (len:%s)' % len(running_games)
            running_games.append(game)

        context['games'] = games
        context['opened_games'] = opened_games
        context['running_games'] = running_games
        context['finished_games'] = finished_games
        return {'context': context}


class GameView(LoginRequiredMixin, TemplateView):
    template_name = 'chess_engine/game.html'

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)

        game_id = kwargs['pk']
        game_logic = ChessLogic.ChessGame(game_id)
        if game_logic:

            context['user_is_creator'] = False
            creator_id = int(game_logic.game_data.get_data('game_options/creator'))
            if creator_id == self.request.user.id:
                context['user_is_creator'] = True

            context['user_can_play'] = False
            side = game_logic.game_data.get_data('token/step/side')
            if side:
                player_id = game_logic.game_data.get_data('participants/%s/1' % side)
                if player_id and player_id == self.request.user.id:
                    context['user_can_play'] = True

                html_board = game_logic.board.render(context)
                context['html_board'] = html_board
            else:
                rounds = game_logic.game_data.get_data('rounds')
                white_wins = 0
                black_wins = 0
                if rounds:
                    for round_k, round in rounds.items():
                        if round['winner'] == 'white':
                            white_wins += 1
                        elif round['winner'] == 'black':
                            black_wins += 1
                context['game_results'] = {
                    'white_wins': white_wins,
                    'black_wins': black_wins
                }
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
        if action == 'surrender_checkmate':
            game_logic.accept_checkmate()
        elif action == 'declare_withdraw':
            game_logic.accept_checkmate()
        elif action == 'declare_draw':
            game_logic.declare_draw()
        elif action == 'reset_round':
            game_logic.reset_round()
        elif action == 'reset_game':
            game_logic.reset_game()

        return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))


class CreateChessGameView(LoginRequiredMixin, FormView):
    template_name = 'chess_engine/game_create_form.html'
    form_class = CreateChessGameForm
    model = GamePersistentData

    def get_form_kwargs(self):
        kwargs = super(CreateChessGameView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        (status, msg) = form.execute()

        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('home'))


class JoinGameView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs['pk']
        side = self.kwargs['side']

        games = GamePersistentData.objects.filter(id=game_id)
        if games.count() != 1:
            print 'Unknown game'
            return HttpResponseRedirect(reverse('home'))

        if side == 'w':
            side = 'white'
        elif side == 'b':
            side = 'black'
        else:
            print 'Unknown side'
            return HttpResponseRedirect(reverse('home'))

        game = games.first()
        game.set_data('participants/%s/1' % side, self.request.user.id)

        return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))
