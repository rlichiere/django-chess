from __future__ import unicode_literals
import json
import math
import yaml

from django.db import models
from django.contrib.auth.models import User

from chess_engine.chess_classes import ChessUtils
from utils import utils
from django_chess import config

# Create your models here.


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj)


class PersistentObject (models.Model):
    data = models.TextField(default='{}')

    def __str__(self):
        return str(self.id)

    def get_data(self, path=None):
        """ loads data, from given key if specified """
        """ - path : url-style, leaf content is returned.
                if no path specified, all data is returned """
        data = json.loads(self.data)
        if path:
            return utils.access(data, path)
        else:
            return data

    def set_data(self, path, new_data):
        """ writes data, at given path if specified """
        """ - data : dict """
        """ - path : url-style, leaf content is set.
                if no path specified, data is written at root """
        if path:
            # write data in path
            data = json.loads(self.data)
            utils.access(data, path, new_data)
            self.data = json.dumps(data, separators=(',', ':'), cls=MyEncoder)
        else:
            # write data at root
            self.data = json.dumps(new_data, separators=(',', ':'), cls=MyEncoder)
        self.save()
        return True

    def pop_data(self, path, key):
        """ pops item designed by path """
        item = self.get_data(path)
        if item:
            result = dict()
            for k, v in item.items():
                if k != key:
                    result[k] = v
            self.set_data(path, result)
            return True
        return False

    def add_item(self, path, key, data, rule='%02d'):
        items = self.get_data('%s/%s' % (path, key))
        if not items:
            items = dict()
        new_key = rule % (len(items) + 1)
        items[new_key] = data
        self.set_data('%s/%s' % (path, key), items)
        return True


class GamePersistentData (PersistentObject):

    def add_log(self, move_data):
        side = move_data['source_piece'].side.name[0:1]
        official = ChessUtils.build_official_move(move_data)
        log_data = {
            'side': side,
            'official': official,
            'source': {
                'piece': move_data['source_piece'],
                'x': move_data['src_x'],
                'y': move_data['src_y']
            },
            'target': {
                'x': move_data['dest_x'],
                'y': move_data['dest_y']
            }
        }
        if 'target_piece' in move_data:
            log_data['target']['piece'] = move_data['target_piece']

        # auto-logging
        if self.get_data('game_options/logging') == 'on':
            log_data['board'] = self.get_data('board')
            token = self.get_data('token')
            if 'logs' in token:
                token['logs'] = '-'
            log_data['token'] = token
            print 'GamePersistentData.add_log: board saved.'

        self.add_item('token', 'logs', log_data, '%03d.')


class UserColorSet(PersistentObject):
    user = models.ForeignKey(User)


class UserRanking(PersistentObject):
    user = models.ForeignKey(User)

    def get_elo(self, game_type):
        return self.get_data('%s/elo' % game_type)

    def get_history(self, game_type):
        return self.get_data('%s/history' % game_type)

    def update_elo(self, game_type, w, d, game_id, opponent_id, opponent_elo):

        old_elo = self.get_elo(game_type)
        if not old_elo:
            old_elo = 0
        else:
            old_elo = int(old_elo)
        user_history = self.get_history(game_type)
        if not user_history:
            user_history = dict()
        if len(user_history) <= 30:
            k = 40
        elif old_elo < 2400:
            k = 30
        else:
            k = 10
        pd = RankingUtils().get_elo_pd(d)
        new_elo = int(old_elo + k * (w - pd))
        elo_delta = int(new_elo) - old_elo
        if new_elo < 0:
            new_elo = '0'
        self.set_data('%s/elo' % game_type, new_elo)

        history_data = {
            'old_elo': old_elo,
            'new_elo': new_elo,
            'elo_delta': elo_delta,
            'k': k,
            'w': w,
            'pd': pd,
            'opponent_id': opponent_id,
            'opponent_elo': opponent_elo,
            'game_id': game_id
        }
        self.set_data('%s/history/%d' % (game_type, len(user_history)), history_data)
        return new_elo

    def get_user_level(self, game_type):

        user_elo = int(self.get_elo(game_type))
        if not user_elo:
            return False

        settings_path = '%s/core/config/settings.yml' % config.PROJECT_ROOT
        level_gaps = yaml.load(open(settings_path))['levels']
        user_level = level_gaps[0]
        previous_elo = 0
        level_k = 0
        user_level['id'] = 0

        # todo : should be done reverse
        for level in level_gaps:
            if previous_elo < level['elo'] < user_elo:
                previous_elo = level['elo']
                user_level = level
                user_level['id'] = level_k
            level_k += 1
        return user_level


class RankingUtils:
    def __init__(self):
        pass

    def get_elo_pd(self, d):
        if d > 400:
            d = 400
        expo = float(0 - d) / float(400)
        quot = 1 + math.pow(10, expo)
        return 1 / quot

    def parse_history_data(self, game_type, user):
        result = dict()

        user_ranking = UserRanking.objects.filter(user=user).first()
        victories = 0
        defeats = 0
        user_ranking_history = user_ranking.get_history(game_type)
        if user_ranking_history:
            for game_k, game in user_ranking_history.items():
                if 'w' in game:
                    w_value = game['w']
                    if w_value == 1:
                        victories += 1
                    elif w_value == 0:
                        defeats += 1
        result['victories'] = victories
        result['defeats'] = defeats
        if defeats != 0:
            result['ratio'] = round(float(victories) / float(defeats), 2)
        else:
            result['ratio'] = victories
        return result
