from json2html import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import View, TemplateView, FormView

from chess_classes import ChessLogic, ChessBoard
from .forms import *
from .models import *
from utils import user_utils


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'chess_engine/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_utils.add_generic_context(context, request=self.request)
        user_utils.add_theme_list(context)

        target_user_id = kwargs['pk']
        target_user = User.objects.filter(id=target_user_id).first()
        if not target_user:
            return False
        context['target_user'] = target_user

        # performances
        perfs = dict()
        user_ranking = UserRanking.objects.get_or_create(user=self.request.user)[0]
        user_elo = user_ranking.get_elo('chess')
        if user_elo:
            perfs['elo'] = user_elo
            perfs['level'] = user_ranking.get_user_level('chess')

        context['performances'] = perfs
        parsed_perf_data = RankingUtils().parse_history_data('chess', target_user)
        context['performances_parsed'] = parsed_perf_data

        # search user games
        context['player_history'] = ProfileLoadData().get_player_history(target_user_id)

        user_colorset = UserColorSet.objects.filter(user=target_user).first()
        if not user_colorset:
            user_colorset = UserColorSet(user=target_user)
            default_colorset = ChessBoard.BoardColorSet().get_default_colorset()
            user_colorset.set_data('chess', default_colorset)
        context['user_customization'] = user_colorset.get_data('')

        return {'context': context}

    def get(self, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        if not context:
            return HttpResponseRedirect(reverse('login'))
        return super(ProfileView, self).get(*args, **kwargs)


class ProfileLoadData(LoginRequiredMixin, TemplateView):
    template_name = 'chess_engine/profile_history.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileLoadData, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        target_user_id = self.request.POST['target_user_id']
        filter_rank = self.request.POST['filter_rank']

        player_history = self.get_player_history(target_user_id=target_user_id, filter_rank=filter_rank)

        context['player_history'] = player_history
        context['target_user_id'] = target_user_id
        context['filter_rank'] = filter_rank
        template_context = dict()
        template_context['context'] = context

        html_result = loader.get_template(self.template_name).render(template_context)
        return HttpResponse(html_result)

    def get_player_history(self, target_user_id, filter_rank=None):
        history = list()
        games = GamePersistentData.objects.all()
        for game in games:
            user_side = False

            game_ranked = game.get_data('game_options/ranked')
            if filter_rank == 'ranked' and not game_ranked:
                continue
            if filter_rank == 'unranked' and game_ranked:
                continue

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
                elif user_side == 'both':
                    opponent_id = game.get_data('participants/black/1')
                else:
                    print 'warning: unknown opponent for user_side %s' % user_side
                    opponent_id = 1
                opponent = User.objects.get(id=opponent_id)
                game_result['player_opponent'] = opponent

                if user_side == 'both':
                    game_result['player_result'] = 'both'
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
        return history


class ProfileShowRankingHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'chess_engine/show_history.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileShowRankingHistoryView, self).get_context_data()
        target_user_id = kwargs['pk']
        target_user = User.objects.filter(id=target_user_id).first()
        if not target_user:
            print 'unknown user : %s' % target_user_id
            return context

        history = list()
        history_type = kwargs['type']
        if history_type == 'ranked':
            user_ranking = UserRanking.objects.filter(user=target_user).first()
            user_history = user_ranking.get_history('chess')
            if user_history:
                for game_index, game_history in user_history.items():
                    if 'game_id' in game_history:
                        game = GamePersistentData.objects.filter(id=game_history['game_id']).first()
                        game_history['game'] = game
                    if 'elo_delta' in game_history:
                        delta = game_history['elo_delta']
                        if delta > 0:
                            game_history['elo_delta'] = '+%s' % delta
                    if 'opponent_id' in game_history:
                        opponent = User.objects.filter(id=game_history['opponent_id']).first()
                        game_history['opponent'] = opponent
                        opponent_ranking = UserRanking.objects.filter(user=opponent).first()
                        if opponent_ranking:
                            opponent_elo = opponent_ranking.get_elo('chess')
                            game_history['opponent_elo'] = opponent_elo
                    history.append(game_history)
        else:
            print 'unknown type : %s' % type
        context['history'] = history
        return context


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
        update_type = kwargs['update_type']
        key = kwargs['key']
        value = kwargs['value']
        print 'ProfileUpdateKeyView.get: key:%s, value:%s' % (key, value)

        user_colorset = UserColorSet.objects.filter(user=user_id).first()
        if key == 'reset':
            if value == 'color_set':
                user_colorset.set_data('%s' % update_type, ChessBoard.BoardColorSet().get_default_colorset())
        else:
            user_colorset.set_data('%s/%s' % (update_type, key), value)
        return HttpResponseRedirect(reverse('profile', kwargs={'pk': self.kwargs['pk']}))


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'chess_engine/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user_utils.add_generic_context(context, request=self.request)

        games = GamePersistentData.objects.all()
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
            if not step:
                finished_games.append(game)
                continue

            rounds = game.get_data('rounds')
            if not rounds:
                running_games.append(game)
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
                finished_games.append(game)
                continue

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
        user_utils.add_generic_context(context, request=self.request)

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

                # add contextual data
                if game_logic.board.is_kingchecked(side):
                    context['king_check'] = side
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

        elif action == 'update_option':
            option_name = kwargs['name']
            option_value = kwargs['value']
            game_logic.game_data.set_data('game_options/%s' % option_name, option_value)

        elif action == 'save_board':
            comment = kwargs['value']
            saved_game = {
                'comment': comment,
                'board': game_logic.game_data.get_data('board'),
                'token': game_logic.game_data.get_data('token')
            }
            saved_games = game_logic.game_data.get_data('saved_games')
            new_index = 1
            if saved_games:
                new_index = len(saved_games) + 1
            new_index = '%03d.' % new_index
            game_logic.game_data.set_data('saved_games/%s' % new_index, saved_game)
        elif action == 'load_previous_log':
            token_logs = game_logic.game_data.get_data('token/logs')
            if token_logs:
                token_logs_len = len(token_logs)
                if token_logs_len > 1:
                    previous_log_index = '%03d.' % (token_logs_len - 1)
                    kwargs['action'] = 'restore_log'
                    kwargs['name'] = '_'
                    kwargs['value'] = previous_log_index
                    return HttpResponseRedirect(reverse('menu-action', kwargs=kwargs))
                else:
                    kwargs['action'] = 'reset_round'
                    return HttpResponseRedirect(reverse('menu-action', kwargs=kwargs))
            else:
                print 'no logs to restore'
        elif action == 'restore_log':
            log_index = kwargs['value']
            self._restore_log(source='logs', log_index=log_index, game_logic=game_logic)
        elif action == 'restore_saved_game':
            log_index = kwargs['value']
            self._restore_log(source='saved_games', log_index=log_index, game_logic=game_logic)
        else:
            print 'unknown action : %s' % action

        return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game_id}))

    def _restore_log(self, source, log_index, game_logic):
        if source == 'saved_games':
            restored_board = game_logic.game_data.get_data('saved_games/%s/board' % log_index)
            restored_token = game_logic.game_data.get_data('saved_games/%s/token' % log_index)
        elif source == 'logs':
            restored_board = game_logic.game_data.get_data('token/logs/%s/board' % log_index)
            restored_token = game_logic.game_data.get_data('token/logs/%s/token' % log_index)

            # backup current logs
            token_logs = game_logic.game_data.get_data('token/logs')
            if token_logs:
                # clean inappropriate logs
                cleaned_logs = dict()
                for token_log_key, token_log in token_logs.items():
                    if int(token_log_key[:-1]) <= int(log_index[:-1]):
                        cleaned_logs[token_log_key] = token_log
                restored_token['logs'] = cleaned_logs
            else:
                print 'restore_log. no token_logs restored ?'
        else:
            print 'error : unknown source : %s' % source
            return False

        if restored_board and restored_token:
            game_logic.game_data.set_data('board', restored_board)
            game_logic.game_data.set_data('token', restored_token)
        else:
            print '*** warning *** restore error: board:%s, token:%s' % (restored_board, restored_token)
            return False
        return True


class CreateChessGameView(LoginRequiredMixin, FormView):
    template_name = 'chess_engine/game_create_form.html'
    form_class = CreateChessGameForm
    model = GamePersistentData

    def get_form_kwargs(self):
        kwargs = super(CreateChessGameView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        (status, game) = form.execute()
        return HttpResponseRedirect(reverse('chess-game', kwargs={'pk': game.id}))

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
