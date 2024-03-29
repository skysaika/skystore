from django.conf import settings
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from django.core.exceptions import ValidationError

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
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name='url')
    image = models.ImageField(upload_to='products/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='цена')
    available = models.BooleanField(default=True, verbose_name='в наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлен')
    # связь с текущим юзером
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')
    # признак публикации
    is_published = models.BooleanField(default=False, verbose_name='опубликован')


    def get_absolute_url(self):
        return reverse('catalog:product_detail',
                       args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:  # генерировать slug только если он еще не установлен
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def active_version(self):
        return self.versions.filter(active_version=True).first()

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        permissions = (
            ('can_publish', 'Может публиковать'),
        )

    def __str__(self):
        return f'{self.name}'


class Version(models.Model):
    """Модель версия продукта"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions', verbose_name='продукт')
    version_number = models.IntegerField(default=1, verbose_name='номер версии')
    version_name = models.CharField(max_length=200, verbose_name='название версии')
    active_version = models.BooleanField(default=False, verbose_name='активная версия')

    def __str__(self):
        return f'{self.active_version} {self.version_number} {self.version_name}'

    class Meta:
        verbose_name = 'версия продукта'
        verbose_name_plural = 'версии продуктов'


