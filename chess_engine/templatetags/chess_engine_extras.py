import json
from json2html import *

from django import template

from utils import utils

register = template.Library()


@register.filter
def render_json2html(value, path):
    jdata = json.loads(value)
    data = utils.access(jdata, path)
    return json2html.convert(json=data)
