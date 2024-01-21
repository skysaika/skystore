from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Админская команда для создания пользователя'

    def handle(self, *args, **options):

        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Sky',
            last_name='Pro',
            is_staff=True,
            is_superuser=True,
        )
        # зададим пароль
        user.set_password('123qwe456rty')
        # сохраняем
        user.save()
