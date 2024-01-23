from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import AuthForm
from chess_engine.views import *
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chess_engine.urls')),
    path('login/', LoginView.as_view(template_name='chess_engine/login.html', authentication_form=AuthForm), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update_password/', ProfileUpdatePasswordView.as_view(), name='update-password'),
    path('profile/<int:pk>/history/<str:type>/', ProfileShowRankingHistoryView.as_view(), name='show-history'),
    path('profile/<int:pk>/load_data/', ProfileLoadData.as_view(), name='profile-load-data'),
    path('profile/<int:pk>/<str:update_type>/<str:key>/<str:value>/', ProfileUpdateKeyView.as_view(), name='profile-update-key'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),
    path('documentation/', DocumentationView.as_view(), name='documentation')
]

