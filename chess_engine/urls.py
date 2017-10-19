from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^game/add$', views.CreateChessGameView.as_view(), name='create-game'),
    url(r'^game/join_game/(?P<pk>[0-9]+)/(?P<side>[wb])$', views.JoinGameView.as_view(), name='join-game'),
    url(r'^game/(?P<pk>[0-9]+)$', views.GameView.as_view(), name='chess-game'),
    url(r'^game/(?P<pk>[0-9]+)/board/cell_click/(?P<action>[a-z]+)/(?P<line>[0-9]+)/(?P<column>[a-h]+)$',
        views.PieceActionView.as_view(), name='piece-action'),
    url(r'^game/(?P<pk>[0-9]+)/board/promote/(?P<role_name>[QRBH])$',
        views.PiecePromoteView.as_view(), name='piece-promote'),
    url(r'^game/(?P<pk>[0-9]+)/menu/(?P<action>[a-z_]+)/(?P<name>[a-z_-]+)/(?P<value>[0-9a-zA-Z_.-]+)$',
        views.MenuView.as_view(), name='menu-action'),
]
