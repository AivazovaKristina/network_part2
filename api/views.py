from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from .pagination import CustomLimitOffsetPagination

from rest_framework import filters, status, viewsets, serializers
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt import tokens

from .permissions import IsAdmin, IsAdminOrReadOnly, IsModeratorOrReadOnly, IsAuthorOrReadOnly, MyCustomPermissionClass
from content.models import Category, Genre, Title, Review, Comment
from users.models import User
from .filters import TitleFilter
from .serializers import (
UserEmailRegistration,
UserConfirmation,
UserSerializer,
CategorySerializer,
GenreSerializer,
TitleWriteSerializer,
TitleReadSerializer,
ReviewsSerializer,
CommentsSerializer,
)


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = serializers.UserEmailRegistration(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    user = User.objects.get_or_create(email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Confirmation_code',
              f'Your confirmation code: {confirmation_code}',
              'christina.aivazova@gmail.com',
              [email])
    return Response(f'The code was sent to the address {email}',
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = serializers.UserConfirmation(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = tokens.AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Invalid confirmation code'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]
    pagination_class = CustomLimitOffsetPagination

    @action(methods=['patch', 'get'],
            permission_classes=[IsAuthenticated],
            detail=False,
            url_path='me',
            url_name='me')
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class ModelMixinSet(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                    GenericViewSet):
    pass


class CategoryViewSet(ModelMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [SearchFilter]
    search_fields = ['=name', ]
    lookup_field = 'slug'
    pagination_class = CustomLimitOffsetPagination


class GenreViewSet(ModelMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    pagination_class = CustomLimitOffsetPagination



class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    filterset_class = TitleFilter
    pagination_class = CustomLimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [MyCustomPermissionClass]
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review_set.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)



class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [MyCustomPermissionClass]
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comment_set.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
