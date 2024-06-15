from django.db import transaction
from rest_framework import views, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import *
from .neural.connect import tokenize, classify, transformer
from .permissions import *
from .serializers import *


class UserListView(views.APIView):
    """Получение списка пользователей"""

    # permission_classes = (IsSuperuserOrPost,)

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
        # try:
        #     user = User.objects.get(pk=pk)
        # except User.DoesNotExist:
        #     raise NotFound(detail="User not found", code=status.HTTP_404_NOT_FOUND)
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


class AnswerView(views.APIView):
    """Получение ответа на запрос"""

    """
    С целью упрощения взаимодействия с api и ускорения работы
    создано одно представление, инициализирующее сущности
    Request, Word и все остальные.
    """

    @transaction.atomic
    def get(self, request):
        message = request.data.get('message', '')
        if not message:
            return Response({'error': 'Message cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        req = Request.objects.create(content=message)

        tokens = tokenize(message)
        words_to_create = [Word(word=token, request=req) for token in tokens]
        Word.objects.bulk_create(words_to_create)

        words = [word.word for word in req.words.all()]

        file_name, title_name = classify(words)
        file = get_object_or_404(File, name=file_name)
        title = get_object_or_404(Title, name=title_name)

        # Использование prefetch_related для предварительной загрузки связанных объектов
        docs = Doc.objects.filter(file=file, title=title).select_related('answer')
        answers = [doc.answer.content for doc in docs]
        prefered_answer = transformer(message, answers)

        answer, created = Answer.objects.get_or_create(content=prefered_answer)
        req.answer = answer
        req.save()

        return Response({'answer': prefered_answer}, status=status.HTTP_200_OK)


class DocViewSet(viewsets.ModelViewSet):
    """Получение доступа к документации"""
    queryset = Doc.objects.all()
    serializer_class = DocSerializer


class RequestViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение достопа к запросам только на чтение"""
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
