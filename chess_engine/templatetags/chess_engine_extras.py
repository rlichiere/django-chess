import json
from json2html import *

from django import template
from django.contrib.auth.models import User

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
def get_user(value):
    users = User.objects.filter(id=value)
    if users.count() == 1:
        return users.first()
    return False
