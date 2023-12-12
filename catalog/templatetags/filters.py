from django import template

register = template.Library()


@register.filter
def mediapath(value):
    """Фильтр для получения пути к изображению"""
    if value:
        return f'/media/{value}'
    else:
        return '#'
# после этого добавила {% load filters %} в подшаблон catalog/includes/inc_product_card.html
