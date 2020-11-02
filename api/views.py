# почистить и сгруппировать импорты
from functools import partial
from rest_framework import viewsets, filters, mixins, status, views, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from django_filters.rest_framework import DjangoFilterBackend
import django_filters.rest_framework
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework import viewsets, status, views
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.decorators import action
from api_yamdb.settings import SIMPLE_JWT
from django.db.models import Avg

from .filters import TitleFilter
from .user_action_permissions import IsAdministratorOrSuperUser
#from .permissions import IsOwnerOrReadOnly
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .models import User
from .models import Title, Comment, Review, Category, Genre
from .serializers import (
    CommentSerializer, ReviewSerializer,
    UserSerializer, EmailSerializer, GetAccessParTokenSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer_get, TitleSerializer_post
)


def send_mail_to_email(to, subject, body):
    """
    Отправляет EMAIL по адресу TO:
    c темой SUBJECT:
    и телом письма BODY:
    """
    send_mail(subject=subject, message=body, from_email='a@ya.ru', recipient_list=[to])


class UserViewSet(viewsets.ModelViewSet):
    """
    Для работы с пользователями (чтение, создание, обновление)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdministratorOrSuperUser,
        ]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch', ], permission_classes=[IsAuthenticated, ])
    def me(self, request, **kwargs):
        """
        Обрабатывает users/me/
        """
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class GetConfirmCodeView(views.APIView):
    """
    Запрос на получение confirmation_code,
    если есть такой пользователь отправляем на присланный EMAIL код подтвержения.
    Код подтверждения формируется как токен JWT с payload пользователя
    """
    serializer_class = EmailSerializer

    def action(self, user, token, serializer):
        """
        Формирует код подтвержения, в него вставляется payload
        пользователя user, отправляет EMAIL,
        возвращаеет email в ответ.
        """
        confirmation_code = token.encode(user.get_payload())
        send_mail_to_email(
            user.email,
            'Confirmation code',
            f'Confirmation code is\n{confirmation_code}\n '
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        проверяет полноту данных запроса,
        по email находит в БД пользователя user,
        если такой находится выполняет действия action
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, email=request.data.get('email'))
            token = TokenBackend(
                SIMPLE_JWT['ALGORITHM'],
                signing_key=SIMPLE_JWT['SIGNING_KEY'],
            )
            return self.action(user, token, serializer)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAuthPairToken(GetConfirmCodeView):
    """
    Запрос пары токенов JWT (refresh, access)  по EMAIL и коду подтвержения.
    Код подтвержения имеет полезную нагрузку payload,
    по ней идентифицируем пользователя,
    которому был этот код сформирован.
    Предварительные действия при post  аналогичны GetConfirmCodeView,
    отличия вынесены в action
    """
    serializer_class = GetAccessParTokenSerializer

    def action(self, user, token, serializer):
        """
        Проверяет соответствие payload из confirmation_code
        и payload пользователя определенного по email.
        формирует пару JWT-токена доступа.
        """
        payload = token.decode(self.request.data.get('confirmation_code'))
        if payload == user.get_payload():
            refresh = RefreshToken.for_user(user)
            return Response(
                {'refresh': str(refresh), 'access': str(refresh.access_token), },
                status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetConfirmCodeView(views.APIView):
    """
    Запрос на получение confirmation_code,
    если есть такой пользователь отправляем на присланный EMAIL код подтвержения.
    Код подтверждения формируется как токен JWT с payload пользователя
    """
    serializer_class = EmailSerializer

    def action(self, user, token, serializer):
        """
        Формирует код подтвержения, в него вставляется payload
        пользователя user, отправляет EMAIL,
        возвращаеет email в ответ.
        """
        confirmation_code = token.encode(user.get_payload())
        send_mail_to_email(
            user.email,
            'Confirmation code',
            f'Confirmation code is\n{confirmation_code}\n '
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        проверяет полноту данных запроса,
        по email находит в БД пользователя user,
        если такой находится выполняет действия action
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, email=request.data.get('email'))
            token = TokenBackend(
                SIMPLE_JWT['ALGORITHM'],
                signing_key=SIMPLE_JWT['SIGNING_KEY'],
            )
            return self.action(user, token, serializer)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAuthParToken(GetConfirmCodeView):
    """
    Запрос пары токенов JWT (refresh, access)  по EMAIL и коду подтвержения.
    Код подтвержения имеет полезную нагрузку payload,
    по ней идентифицируем пользователя,
    которому был этот код сформирован.
    Предварительные действия при post  аналогичны GetConfirmCodeView,
    отличия вынесены в action
    """
    serializer_class = GetAccessParTokenSerializer

    def action(self, user, token, serializer):
        """
        Проверяет соответствие payload из confirmation_code
        и payload пользователя определенного по email.
        формирует пару JWT-токена доступа.
        """
        payload = token.decode(self.request.data.get('confirmation_code'))
        if payload == user.get_payload():
            refresh = RefreshToken.for_user(user)
            return Response(
                {'refresh': str(refresh), 'access': str(refresh.access_token), },
                status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    """C пермишенами разобраться"""

    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleSerializer_get
        return TitleSerializer_post



class CategoryViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   ):
    """C пермишенами разобраться"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   ):
    """C пермишенами разобраться"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']



class ReviewViewSet(viewsets.ModelViewSet):
    """***"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly,

    ]
    lookup_field = 'pk'


    def get_serializer_context(self):
        """передача дополнительных аргументов"""
        context = super(ReviewViewSet, self).get_serializer_context()
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        context.update({'title': title})
        return context

    def perform_create(self, serializer):
        """***"""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


    def get_queryset(self):
        """***"""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """***"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly,
    ]


    def get_queryset(self):
        """***"""

        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        """***"""

        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(review=review, author=self.request.user)
