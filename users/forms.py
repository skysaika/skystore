from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2') # 2 пароля


class UserForm(StyleFormMixin, UserChangeForm):
    """Форма редактирования профиля"""
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'avatar', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        """Спрячем пароль"""
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
