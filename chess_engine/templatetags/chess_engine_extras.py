import json
from json2html import *

from django import template
from django.contrib.auth.models import User
from chess_engine.models import *

from utils import utils

register = template.Library()


@register.filter
def render_json2html(value, path):
    jdata = json.loads(value)
    data = utils.access(jdata, path)
    return json2html.convert(json=data)


@register.filter
def render_realjson2html(value, path):
    data = utils.access(value, path)
    return json2html.convert(json=data)


@register.filter
def access(value, path):
    jdata = json.loads(value)
    data = utils.access(jdata, path)
    return data


@register.filter
def get_user(user_id):
    if not user_id:
        return False
    user = User.objects.filter(id=user_id).first()
    if not user:
        return False
    return user


@register.filter
def can_join_game(user, game):
    if not user or not game:
        return False
    if game.id == 138:
        print '@filter: game : %s' % game
        print '@filter: game_options/ranked : %s' % game.get_data('game_options/ranked')

    if game.get_data('game_options/ranked'):
        print 'this game is ranked.'
        if user.id in [int(game.get_data('participants/white/1')), int(game.get_data('participants/black/1'))]:
            return False
    return True
