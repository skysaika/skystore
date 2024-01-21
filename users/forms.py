from django.contrib.auth.forms import UserCreationForm

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2') # 2 пароля
