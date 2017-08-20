from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^game/(?P<id>[0-9]+)$', views.GameView.as_view(), name='game'),
    url(r'^game/(?P<id>[0-9]+)/click/(?P<action>[a-z]+)/(?P<line>[0-9]+)/(?P<column>[a-h]+)$',
        views.PieceActionView.as_view(), name='piece-action'),
]
