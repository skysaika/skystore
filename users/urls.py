from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # маршрут для входа
    path('logout/', LogoutView.as_view(), name='logout'),  # маршрут для выхода
    path('register/', RegisterView.as_view(), name='register'),  # контроллер для регистрации
]
