from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title

from .custom_mixin import CustomMixin
from .filters import TitleFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthor
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateTitleSerializer, GenreSerializer,
                          GetTitleSerializer, ReviewSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor, )
    pagination_class = CustomPagination

    def get_queryset(self):
        pk = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=pk)
        # just a comment
        return review.comments.all()

    def perform_create(self, serializer):
        review_pk = self.kwargs.get('review_id')
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(title.reviews, id=review_pk)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class GenresViewSet(CustomMixin):
    queryset = Genre.objects.all()
    pagination_class = CustomPagination
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoryViewSet(CustomMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = GetTitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetTitleSerializer
        return CreateTitleSerializer
