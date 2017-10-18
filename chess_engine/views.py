from json2html import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView, FormView

from chess_classes import ChessLogic, ChessBoard
from .forms import *
from .models import *


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'chess_engine/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        target_user_id = kwargs['pk']
        target_user = User.objects.filter(id=target_user_id).first()
        if not target_user:
            return False
        context['target_user'] = target_user

        # search user games
        history = list()
        games = GamePersistentData.objects.all()
        for game in games:
            user_side = False
            whites = game.get_data('participants/white')
            if whites:
                for white_k, white in whites.items():
                    if int(white) == int(target_user_id):
                        user_side = 'white'
            blacks = game.get_data('participants/black')
            if blacks:
                for black_k, black in blacks.items():
                    if int(black) == int(target_user_id):
                        if user_side:
                            user_side = 'both'
                        else:
                            user_side = 'black'
            if user_side:
                game_result = dict()
                game_result['data'] = game
                game_result['player_side'] = user_side

                winner = game.get_data('result/winner')
                if not winner:
                    continue

                # retrieve opponent
                if user_side == 'white':
                    opponent_id = game.get_data('participants/black/1')
                elif user_side == 'black':
                    opponent_id = game.get_data('participants/white/1')
                else:
                    print 'warning: unknown opponent for user_side %s' % user_side
                    opponent_id = 1

                opponent = User.objects.get(id=opponent_id)
                game_result['player_opponent'] = opponent

                if user_side == 'both':
                    game_result['player_result'] = '-'
                elif winner == user_side:
                    game_result['player_result'] = 'win'
                else:
                    game_result['player_result'] = 'lost'

                round_list = game.get_data('result/round_list')
                if round_list:
                    game_result['round_list'] = round_list
                    player_round_list = ''
                    for c in round_list:
                        if c == user_side[:1]:
                            player_round_list += 'W'
                        else:
                            player_round_list += 'L'
                    game_result['player_round_list'] = player_round_list

                history.append(game_result)
        context['player_history'] = history

        user_colorset = UserColorSet.objects.filter(user=target_user).first()
        if not user_colorset:
            user_colorset = UserColorSet(user=target_user)
            default_colorset = ChessBoard.BoardColorSet().get_default_colorset()
            user_colorset.set_data('chess', default_colorset)
        context['color_set'] = user_colorset.get_data('chess')

        return {'context': context}

    def get(self, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        if not context:
            return HttpResponseRedirect(reverse('login'))
        return super(ProfileView, self).get(*args, **kwargs)


class ProfileUpdatePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'chess_engine/update_password.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdatePasswordView, self).get_context_data()
        context['target_user_id'] = kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        user_target_id = kwargs['pk']
        new_password = request.POST['password']

        if request.user.is_superuser:
            print 'Superuser cannot change its password here.'
            return HttpResponseRedirect('/profile/%s' % user_target_id)

        if int(user_target_id) != request.user.id and not request.user.is_superuser:
            print 'Only superuser can change other users password.'
            return HttpResponseRedirect('/profile/%s' % user_target_id)

        try:
            user = User.objects.filter(id=user_target_id).first()
            if not user:
                return HttpResponseRedirect('/profile/%s' % user_target_id)
            else:
                user.set_password(new_password)
                user.save()
        except Exception as e:
            return HttpResponseRedirect('/profile/%s' % user_target_id)
        return HttpResponseRedirect('/login')


class ProfileUpdateKeyView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        user_id = kwargs['pk']
        game_type = kwargs['game_type']
        key = kwargs['key']
        value = kwargs['value']

        user_colorset = UserColorSet.objects.filter(user=user_id).first()
        if key == 'reset':
            if value == 'color_set':
                user_colorset.set_data('%s' % game_type, ChessBoard.BoardColorSet().get_default_colorset())
        else:
            user_colorset.set_data('%s/%s' % (game_type, key), value)
        return HttpResponseRedirect(reverse('profile', kwargs={'pk': self.kwargs['pk']}))


class HomeView(LoginRequiredMixin, TemplateView):
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
        game_logic = ChessLogic.ChessGame(user_id=self.request.user, game_id=game_id)
        if not game_logic:
            context['html_board'] = 'Game not found.'
            return {'context': context}
        else:
            context['user'] = self.request.user
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


class PieceActionView(View):

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs['pk']
        action = kwargs['action']
        line_k = kwargs['line']
        column_k = kwargs['column']
        print 'PieceAction.get : game_id : %s, action : %s, line : %s, column : %s' % (game_id, action, line_k, column_k)

        game_logic = ChessLogic.ChessGame(user_id=self.request.user.id, game_id=game_id)
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

        game_logic = ChessLogic.ChessGame(user_id=self.request.user.id, game_id=game_id)
        if not game_logic:
            print ('PieceActionView.get ERROR : game not found : %s' % game_id)
            return HttpResponseRedirect(reverse('home'))

        role_name = kwargs['role_name']
        game_logic.promote_piece(request.user, role_name)
        return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))


class MenuView(View):

    def get(self, request, *args, **kwargs):
        game_id = self.kwargs['pk']
        game_logic = ChessLogic.ChessGame(user_id=self.request.user.id, game_id=game_id)
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
