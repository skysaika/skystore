from django.db import models
from django.urls import reverse
from slugify import slugify

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Category(models.Model):
    """Модель Категория"""
    name = models.CharField(max_length=200, verbose_name='название категории')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    slug = models.SlugField(max_length=200, unique=True, verbose_name='ссылка')

    def save(self, *args, **kwargs):
        if not self.slug:  # Генерация slug только если он не установлен
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:category_list',
                       args=[self.slug])

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]


class Product(models.Model):
    """Модель Продукт"""
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE,
                                 verbose_name='категория')  # related_name имя обратной связи от категории к продукту
    name = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(max_length=200, verbose_name='url')
    image = models.ImageField(upload_to='products/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='цена')
    available = models.BooleanField(default=True, verbose_name='в наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлен')

    def get_absolute_url(self):
        return reverse('catalog:product_detail',
                       args=[self.id, self.slug])

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'{self.name}'
