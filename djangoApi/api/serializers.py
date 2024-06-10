from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from .models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name')


class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = ('id', 'name')


class RequestSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    scope = ScopeSerializer(many=False, read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'content', 'author', 'scope')
