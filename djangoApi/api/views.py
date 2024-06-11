from django.shortcuts import render
from django.db import transaction
from rest_framework import views, status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import *
from .permissions import IsSuperuserOrPost, IsSuperuserOrOwner
from .serializers import UserSerializer, UserCreateSerializer


class UserListView(views.APIView):
    """Получение списка пользователей"""

    permission_classes = (IsSuperuserOrPost,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        user_serializer = UserCreateSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data = user_serializer.data
            data['token'] = token.key
            return Response(data, status=201)
        return Response(user_serializer.errors, status=400)

    # def validate(self, attrs):
    #     if User.objects.filter(username=attrs.get("username")).exists():
    #         raise ValidationError("This username already exists.")
    #     return attrs


class UserDetailView(views.APIView):
    """Взаимодействие с конкретным пользователем"""

    permission_classes = (IsSuperuserOrOwner,)

    def get(self, request, pk):
        # try:
        #     user = User.objects.get(pk=pk)
        # except User.DoesNotExist:
        #     raise NotFound(detail="User not found", code=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        token = get_object_or_404(Token, user=user)
        token.delete()
        user.delete()
        return Response({'message': 'ok'}, status=200)

