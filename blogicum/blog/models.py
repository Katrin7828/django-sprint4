from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from core.models import BaseModel


User = get_user_model()
LENGTH = 256


class Post(BaseModel):
    title = models.CharField(max_length=LENGTH, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='Если установить дату и время в '
                                    'будущем — '
                                    'можно делать отложенные публикации.')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name='Изображение к посту',
        help_text='Загрузите изображение для публикации',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'

    def __str__(self):
        return self.title


class Category(BaseModel):
    title = models.CharField(max_length=LENGTH, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True,
                            verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                            'разрешены символы латиницы, цифры, '
                            'дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(max_length=LENGTH,
                            verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='congratulations',
        verbose_name='Пост',
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор поздравления',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'поздравление'
        verbose_name_plural = 'поздравления'

    def __str__(self):
        return f'Поздравление от {self.author.username} к посту {self.post.
                                                                 title}'


class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    is_approved = models.BooleanField(
        default=True,
        verbose_name='Одобрен',
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.post.title}'
