from django.conf import settings
from django.core.mail import send_mail


def send_new_password(email, new_password):
    """Функция отправки письма с новым паролем"""
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],  # список получателей
    )
