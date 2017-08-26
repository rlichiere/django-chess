from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^game/(?P<pk>[0-9]+)$', views.GameView.as_view(), name='chess-game'),
    url(r'^game/(?P<pk>[0-9]+)/board/cell_click/(?P<action>[a-z]+)/(?P<line>[0-9]+)/(?P<column>[a-h]+)$',
        views.PieceActionView.as_view(), name='piece-action'),
    url(r'^game/(?P<pk>[0-9]+)/board/promote/(?P<role_name>[QRBH])$', views.PiecePromoteView.as_view(), name='piece-promote'),
    url(r'^game/(?P<pk>[0-9]+)/menu/(?P<action>[a-z_]+)/(?P<value>[a-z]+)$', views.MenuView.as_view(), name='menu-action'),
]
