from __future__ import unicode_literals
import json
from django.db import models
from utils import utils
from chess_engine.chess_classes import ChessUtils

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

    def pop_data(self, path):
        """ pops item designed by path """
        item = self.get_data(path)
        # todo : delete path leaf
        return item

    #                'token' 'logs' 'log_xxx': {}
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
        self.add_item('token', 'logs', log_data, '%03d.')
