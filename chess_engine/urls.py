from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('game/add/', views.CreateChessGameView.as_view(), name='create-game'),
    re_path(r'^game/join_game/(?P<pk>[0-9]+)/(?P<side>[wb])$', views.JoinGameView.as_view(), name='join-game'),
    path('game/<int:pk>/', views.GameView.as_view(), name='chess-game'),
    re_path(r'^game/(?P<pk>[0-9]+)/board/cell_click/(?P<action>[a-z]+)/(?P<line>[0-9]+)/(?P<column>[a-h]+)$',
            views.PieceActionView.as_view(), name='piece-action'),
    re_path(r'^game/(?P<pk>[0-9]+)/board/promote/(?P<role_name>[QRBH])$',
            views.PiecePromoteView.as_view(), name='piece-promote'),
    re_path(r'^game/(?P<pk>[0-9]+)/menu/(?P<action>[a-z_]+)/(?P<name>[a-z_-]+)/(?P<value>[0-9a-zA-Z_.-]+)$',
            views.MenuView.as_view(), name='menu-action'),
]
