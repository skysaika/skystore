import uuid

from django.db import models
from pytils.translit import slugify

NULLABLE = {'null': True, 'blank': True}


class VlogPost(models.Model):
    """Модель поста"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='Превью', **NULLABLE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    view_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        """Метод для генерации slug"""
        if not self.slug:
            # если значение slug не задано, создаем его на основе заголовка статьи и случайного UUID
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4().hex[:6])
            # проверяем, что значение slug уникально
            while VlogPost.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.title) + '-' + str(uuid.uuid4().hex[:6])
        else:
            # Если slug уже существует (например, при редактировании), обновляем его только в случае изменения заголовка
            if self.title != VlogPost.objects.get(pk=self.pk).title:
                new_slug = slugify(self.title) + '-' + str(uuid.uuid4().hex[:6])
                # проверяем, что новое значение slug уникально
                while VlogPost.objects.filter(slug=new_slug).exists():
                    new_slug = slugify(self.title) + '-' + str(uuid.uuid4().hex[:6])
                self.slug = new_slug
        super(VlogPost, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created']
        permissions = [
            ('can_publish', 'Может опубликовать'),
        ]
