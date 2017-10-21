import json
from json2html import *

from django import template
from django.contrib.auth.models import User
from chess_engine.models import *

from utils import utils

register = template.Library()


@register.filter
def multiply(left, right):
    return left * right


@register.filter
def get_table_height(lines_number, max_height):
    table_height = 60 + lines_number * 51
    return table_height if table_height < max_height else max_height


@register.filter
def contains_a_line_with_property(data, key_name):
    for line_k, line in data.items():
        if key_name in line:
            return True
    return False


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

    if game.get_data('game_options/ranked'):
        if user.id in [int(game.get_data('participants/white/1')), int(game.get_data('participants/black/1'))]:
            return False
    return True
