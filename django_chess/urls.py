"""django_chess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from django.conf.urls.static import static
from forms import AuthForm
from chess_engine.views import ProfileView, ProfileUpdateKeyView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('chess_engine.urls')),
    url(r'^login/$', views.login, {'template_name': 'chess_engine/login.html', 'authentication_form': AuthForm},
        name="login"),
    url(r'^profile/(?P<pk>[0-9]+)$', ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<pk>[0-9]+)/(?P<game_type>[a-z]+)/(?P<key>[a-zA-Z0-9_]+)/(?P<value>[a-zA-Z0-9- ]+)$',
        ProfileUpdateKeyView.as_view(), name='profile-update-key'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}, name='logout')
]
