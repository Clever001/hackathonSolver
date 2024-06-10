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


MAX_LENGTH_TEXT_FIELD = 5000
User = get_user_model()


class Request(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор запроса',
    )
    scope = models.ForeignKey(
        'Scope',
        on_delete=models.CASCADE,  # SetNull
        verbose_name='Сфера вопроса',
    )
    content = models.CharField(
        max_length=MAX_LENGTH_TEXT_FIELD,
        verbose_name='Текст запроса',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время и дата получения запроса',
    )

    class Meta:
        ordering = ('created',)
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

        default_related_name = 'requests'


class Word(models.Model):
    word = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Слово',
    )
    requests = models.ManyToManyField(
        Request,
        verbose_name='Запросы',
    )

    class Meta:
        ordering = ('word',)
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'

        default_related_name = 'words'


class DocAnswer(models.Model):
    question = models.CharField(
        max_length=MAX_LENGTH_TEXT_FIELD,
        verbose_name='Типовой вопрос',
    )
    answer = models.CharField(
        max_length=MAX_LENGTH_TEXT_FIELD,
        verbose_name='Ответ',
    )
    scope = models.ForeignKey(
        'Scope',
        on_delete=models.CASCADE,
        verbose_name='Сфера вопроса',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'answer'],
                name='unique_question_answer',
            ),
            models.UniqueConstraint(
                fields=['question', 'answer', 'scope'],
                name='unique_question_answer_scope',
            ),
        ]
        ordering = ('answer',)
        verbose_name = 'Типовой вопрос с примером'
        verbose_name_plural = 'Типовые вопросы с примерами'

        default_related_name = 'docAnswers'


class Scope(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название сферы вопросов',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Сфера вопросов'
        verbose_name_plural = 'Cферы вопросов'

        default_related_name = 'scope'
