import pandas as pd
from django.db import transaction
from rest_framework import views, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import *
from .neural.classifier import classify, query_search
from .neural.transform import Bert
from .neural.connect import Classify, Embed
from .permissions import *
from .serializers import *


class UserListView(views.APIView):
    """Получение списка пользователей"""

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


class UserDetailView(views.APIView):
    """Взаимодействие с конкретным пользователем"""

    permission_classes = (IsSuperuserOrOwner,)

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        token = get_object_or_404(Token, user=user)
        token.delete()
        user.delete()
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


def get_dataframe():
    docs = {'name': [], 'content': []}
    for doc in Doc.objects.all():
        docs['name'].append(doc.name)
        docs['content'].append(doc.content)
    docs = pd.DataFrame(docs)
    return docs


class AnswerView(views.APIView):
    """Получение ответа на запрос"""

    @transaction.atomic
    def get(self, request):
        message = request.data.get('message', '')
        if not message:
            return Response({'error': 'Message cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        req_obj = Request.objects.create(content=message)

        docs = get_dataframe()

        if not Embedding.objects.exists():
            emb = Embedding.objects.create()
            emb.set_array(classify(docs))
            emb.save()

        emb = Embedding.objects.first()
        embedding_data = emb.get_array()

        answer = Bert(query_search(embedding=embedding_data, df=docs, query=message))

        ans_obj = Answer.objects.create(content=answer)

        req_obj.answer = ans_obj
        req_obj.save()

        if len(answer.strip()) == 0:
            answer = "Извините, но мы не можем ответить на ваш запрос. Вы можете обратиться на линию тех поддержки."

        return Response({'answer': answer}, status=status.HTTP_200_OK)


class RefreshEmbeddingView(views.APIView):

    @transaction.atomic
    def post(self, request):
        if Embedding.objects.exists():
            emb = Embedding.objects.first()
            emb.delete()

        docs = get_dataframe()

        emb = Embedding.objects.create()
        emb.set_array(classify(docs))
        emb.save()
        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)


class DocViewSet(viewsets.ModelViewSet):
    """Получение доступа к документации"""
    queryset = Doc.objects.all()
    serializer_class = DocSerializer
