from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegisterForm
from users.models import User


class LoginView(BaseLoginView):
    """Контроллер входа"""
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    """Контроллер выхода"""


class RegisterView(CreateView):
    """Контроллер регистрации"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка письма с приветствием при регистрации"""
        new_user = form.save()  # сохраняем пользователя
        send_mail(
            subject='Поздравляем с регистрацией!',
            message='Вы успешно зарегистрировались на аншей платформе.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],  #
        )
        return super().form_valid(form)
