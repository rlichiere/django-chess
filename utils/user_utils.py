import yaml
from django_chess import config
from chess_engine.models import UserColorSet


def add_generic_context(context, request):
    context['user_theme'] = get_user_theme(request.user)
    context['user_pieces'] = get_user_pieces(request.user)


def add_theme_list(context):
    context['available_themes'] = get_themes_list()
    context['available_pieces'] = get_pieces_list()


def get_themes_list():
    settings_path = '%s/core/config/settings.yml' % config.PROJECT_ROOT
    available_themes = yaml.load(open(settings_path))['available_themes']
    return available_themes


def get_levels_list(add_bonuses=None):
    settings_path = '%s/core/config/settings.yml' % config.PROJECT_ROOT
    levels = yaml.load(open(settings_path))['levels']
    level_k = 0

    theme_list = dict()
    piece_list = dict()
    if add_bonuses:
        theme_list = get_themes_list()
        piece_list = get_pieces_list()

    for level in levels:
        level['id'] = level_k
        bonus = dict()
        if add_bonuses:
            for theme in theme_list:
                if 'required_level' in theme:
                    if theme['required_level'] == level_k:
                        bonus['theme'] = theme
                        break
            for piece_set in piece_list:
                if 'required_level' in piece_set:
                    if piece_set['required_level'] == level_k:
                        bonus['piece_set'] = piece_set
                        break
            if len(bonus) > 0:
                level['bonus'] = bonus
        level_k += 1
    return levels


def get_pieces_list():
    settings_path = '%s/core/config/settings.yml' % config.PROJECT_ROOT
    available_pieces = yaml.load(open(settings_path))['available_pieces']
    return available_pieces


def get_user_theme(user):
    user_color_set = UserColorSet.objects.filter(user=user).first()
    if not user_color_set:
        return dict()
    theme_name = user_color_set.get_data('main/theme')
    if not theme_name:
        return dict()

    theme_list = get_themes_list()
    for theme in theme_list:
        if theme['name'] == theme_name:
            return theme
    return dict()


def get_user_pieces(user):
    user_color_set = UserColorSet.objects.filter(user=user).first()
    if not user_color_set:
        return dict()
    user_pieces_name = user_color_set.get_data('main/piece_set')

    pieces_list = get_pieces_list()
    if not user_pieces_name:
        return pieces_list[0]

    for piece_set in pieces_list:
        if piece_set['name'] == user_pieces_name:
            return piece_set
    return dict()
