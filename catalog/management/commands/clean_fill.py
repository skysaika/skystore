from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.core.management import call_command  # Импорт функции для вызова других команд

# вручную:
# Сначала создайте фикстуру командой
# python manage.py dumpdata catalog > data2.json
# переложи в папку fixtures, далее можно чистить базу
# python manage.py loaddata data2.json


class Command(BaseCommand):
    """
    Кастомная команда для удаления и заполнения базы данных
    """
    def handle(self, *args, **options):
        # Здесь код для очистки старых данных
        Category.objects.all().delete()
        Product.objects.all().delete()
        # Здесь код для заполнения новыми данными из фикстуры
        call_command('loaddata', 'catalog/fixtures/data.json')  # Замените 'data.json' на имя вашей фикстуры

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with new data'))
        # создай фикстуру командой: python3 manage.py dumpdata catalog > data.json
        # далее запусти кастомную команду чистки и заполнения бд
        # python3 manage.py clean_fill
        # можно дозаполнить json и добавить данные командой: python3 manage.py loaddata data.json
