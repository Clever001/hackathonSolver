from django.db import transaction
from rest_framework import views, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import *
from .neural.connect import tokenize, classify
from .permissions import IsSuperuserOrPost, IsSuperuserOrOwner, RequestDetailPermission, SafeOrSuperuserPermission
from .serializers import UserSerializer, UserCreateSerializer, RequestContentSerializer, ScopeSerializer, \
    DocAnswerSerializer


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


class RequestContentView(views.APIView):
    """Реализация сохранения и просмотра текста запросов"""

    permission_classes = (IsSuperuserOrOwner,)

    def get(self, request):
        if request.user.is_superuser:
            requests = Request.objects.all()
        else:
            requests = Request.objects.filter(author=request.user)
        requests_serializers = RequestContentSerializer(requests, many=True)
        return Response(requests_serializers.data)

    @transaction.atomic
    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        request_serializer = RequestContentSerializer(data=data)
        if request_serializer.is_valid():
            request_serializer.save()
            return Response(request_serializer.data, status=201)
        return Response(request_serializer.errors, status=400)


class RequestContentDetail(views.APIView):
    """Реализация просмотра и удаления конкретного запроса"""

    permission_classes = (RequestDetailPermission,)

    def get(self, request, pk):
        req = get_object_or_404(Request, pk=pk)
        # return Response({"author": req.author.id, "user": request.user.id})
        self.check_object_permissions(request, req)
        serializer = RequestContentSerializer(req, many=False)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk):
        req = get_object_or_404(Request, pk=pk)
        self.check_object_permissions(request, req)
        req.delete()
        return Response({'message': 'ok'}, status=200)


class ScopeViewSet(viewsets.ModelViewSet):
    """Реализация работы с сферами вопросов"""
    queryset = Scope.objects.all()
    serializer_class = ScopeSerializer
    permission_classes = (SafeOrSuperuserPermission,)


class TokenizationView(views.APIView):
    """Реализация токенизации"""

    permission_classes = (RequestDetailPermission,)

    @transaction.atomic
    def post(self, request, pk):
        req = get_object_or_404(Request, pk=pk)
        self.check_object_permissions(request, req)
        content = req.content
        tokens = tokenize(content)
        for token in tokens:
            word = Word.objects.create(word=token, request=req)
            word.save()
        words = [word.word for word in req.words.all()]
        return Response(words, status=201)


class ClassificationView(views.APIView):
    """Реализация классификации"""

    permission_classes = (RequestDetailPermission,)

    @transaction.atomic
    def post(self, request, pk):
        req = get_object_or_404(Request, pk=pk)
        self.check_object_permissions(request, req)
        if not req.words.exists():
            return Response({'message': 'Request is not tokenized'}, status=400)
        words = [word.word for word in req.words.all()]
        scope_id = classify(words)
        req.scope = get_object_or_404(Scope, pk=scope_id)
        req.save()
        req_serializer = RequestContentSerializer(req, many=False)
        return Response(req_serializer.data, status=201)


class DocAnswerViewSet(viewsets.ModelViewSet):
    """Реализация работы с ответами из документации"""
    queryset = DocAnswer.objects.all()
    serializer_class = DocAnswerSerializer
    permission_classes = (SafeOrSuperuserPermission,)


class AnswersView(views.APIView):
    """Реализация получения ответов из заданной области"""

    def get(self, request, scope_id):
        scope = get_object_or_404(Scope, pk=scope_id)
        doc_answers = DocAnswer.objects.filter(scope=scope)
        serializer = DocAnswerSerializer(doc_answers, many=True)
        return Response(serializer.data)
