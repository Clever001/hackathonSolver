from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Размеры берутся с запасом.
MAX_LENGTH_MESSAGE_FIELD = 5000
MAX_LENGTH_TITLE_FIELD = 500
User = get_user_model()


class Request(models.Model):
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор запроса',
    #     # related_name='user',
    # )
    content = models.CharField(
        max_length=MAX_LENGTH_MESSAGE_FIELD,
        verbose_name='Текст запроса',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время и дата создания запроса',
    )
    answer = models.ForeignKey(
        'Answer',
        on_delete=models.CASCADE,
        verbose_name='Документация',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('created',)
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

        default_related_name = 'requests'


class Word(models.Model):
    word = models.CharField(
        max_length=MAX_LENGTH_TITLE_FIELD,
        verbose_name='Слово',
    )
    # В терминах нейронной модели тут содержится токен,
    # но в логике джанго токен обозначает другую сущность.
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        verbose_name='Запрос',
    )

    class Meta:
        ordering = ('word',)
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'

        default_related_name = 'words'


class Answer(models.Model):
    content = models.CharField(
        max_length=MAX_LENGTH_MESSAGE_FIELD,
        verbose_name='Ответы из документации',
        unique=True,  # !!!
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class File(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_TITLE_FIELD,
        verbose_name='Название файла',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_TITLE_FIELD,
        verbose_name='Название заголовка',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовки'


class Doc(models.Model):
    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        verbose_name='Название файла'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название заголовка',
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name='Ответ из документации',
    )

    class Meta:
        verbose_name = 'Документация'
        verbose_name_plural = 'Документация'

        default_related_name = 'doc'
