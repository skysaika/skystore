from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserForm
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

class UserUpdateView(UpdateView):
    """Контроллер редактирования профиля"""
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Метод редактирует текущего пользователя без использваония pk"""
        return self.request.user


def generate_new_password(request):
    """Функция генерации пароля"""
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    # отправка письма с новым паролем:
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],  # список получателей
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))
