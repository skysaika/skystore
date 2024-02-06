from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_category_list_cache():
    """Функция для получения категорий из кэша"""
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = list(Category.objects.all())
            cache.set(key, category_list, 60)  # Кэширование на 60 секунд
            return category_list
        else:
            return Category.objects.all()
        return category_list
