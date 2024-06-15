from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import numpy as np
import pickle


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Размеры берутся с запасом.
MAX_LENGTH_MESSAGE_FIELD = 10000
MAX_LENGTH_TITLE_FIELD = 500
User = get_user_model()


class Request(models.Model):
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


class Answer(models.Model):
    content = models.CharField(
        max_length=MAX_LENGTH_MESSAGE_FIELD,
        verbose_name='Содержание ответа',
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Doc(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_TITLE_FIELD,
        verbose_name='Имя файла',
    )
    content = models.TextField(
        verbose_name='Содержание документа'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Файл документации'
        verbose_name_plural = 'Файлы документации'


class Embedding(models.Model):
    array_data = models.BinaryField(
        verbose_name='Бинарная информация',
    )

    def set_array(self, array):
        self.array_data = pickle.dumps(array)

    def get_array(self):
        return pickle.loads(self.array_data)

    class Meta:
        verbose_name = 'Embedding'
        verbose_name_plural = 'Embedding'


