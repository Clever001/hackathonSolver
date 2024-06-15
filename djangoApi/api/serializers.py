from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from .models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "is_superuser", "date_joined")


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "username", "last_name", "first_name", "email", "password",)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class DocSerializer(serializers.ModelSerializer):
    file = serializers.CharField()
    title = serializers.CharField()
    answer = serializers.CharField()

    class Meta:
        model = Doc
        fields = ('file', 'title', 'answer',)

    def create(self, validated_data):
        file_name = validated_data.pop('file')
        title_name = validated_data.pop('title')
        answer_content = validated_data.pop('answer')

        file, created = File.objects.get_or_create(name=file_name)
        title, created = Title.objects.get_or_create(name=title_name)
        answer, created = Answer.objects.get_or_create(content=answer_content)

        doc = Doc.objects.create(file=file, title=title, answer=answer, **validated_data)
        return doc


class RequestSerializer(serializers.ModelSerializer):
    answer = serializers.CharField()

    class Meta:
        model = Request
        fields = ('content', 'created', 'answer',)
